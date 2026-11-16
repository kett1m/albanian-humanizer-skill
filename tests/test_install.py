"""Exercise the shell installer through a real controlling terminal (Unix)."""
import os
from pathlib import Path
import select
import subprocess
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/albanian-humanizer'


@unittest.skipIf(os.name == 'nt', 'POSIX terminal tests; Windows uses install.ps1')
class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='humanizer install ')
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)

    def run_installer(self, answers, extra=(), command=None, env=None):
        import fcntl
        import termios
        master, slave = os.openpty()

        def terminal():
            os.setsid()
            fcntl.ioctl(0, termios.TIOCSCTTY, 0)

        command = command or ['bash', str(ROOT / 'install.sh'), '--source', str(ROOT), '--project', *extra]
        proc = subprocess.Popen(command, cwd=self.project, stdin=slave, stdout=slave,
                                stderr=slave, preexec_fn=terminal, env=env)
        os.close(slave)
        output = bytearray()
        try:
            os.write(master, answers.encode())
            deadline = time.monotonic() + 15
            while time.monotonic() < deadline:
                if select.select([master], [], [], 0.1)[0]:
                    try:
                        data = os.read(master, 65536)
                    except OSError:
                        break
                    if not data:
                        break
                    output.extend(data)
                elif proc.poll() is not None:
                    break
            if proc.poll() is None:
                proc.wait(timeout=2)
            return proc.returncode, output.decode(errors='replace')
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait()
            os.close(master)

    def assert_complete(self, destination):
        files = {p.relative_to(SKILL) for p in SKILL.rglob('*') if p.is_file()}
        self.assertEqual(files, {p.relative_to(destination) for p in destination.rglob('*') if p.is_file()})
        for name in files:
            self.assertEqual((SKILL / name).read_bytes(), (destination / name).read_bytes())

    def test_piped_script_reads_answers_from_terminal_and_installs_one_target(self):
        command = ['bash', '-o', 'pipefail', '-c',
                   'cat "$1" | bash -s -- --source "$2" --project',
                   '_', str(ROOT / 'install.sh'), str(ROOT)]
        code, output = self.run_installer('2\ny\n', command=command)
        self.assertEqual(code, 0, output)
        self.assertIn('Which AI agent or app do you use?', output)
        self.assert_complete(self.project / '.claude/skills/albanian-humanizer')
        self.assertEqual([p.name for p in self.project.iterdir()], ['.claude'])

    def test_invalid_and_blank_answers_do_not_default_to_an_agent(self):
        code, output = self.run_installer('\nno-such-agent\n1,999\n1,\nq\n')
        self.assertEqual(code, 0, output)
        self.assertEqual(list(self.project.iterdir()), [])
        self.assertEqual(output.count('Choose a listed number or name'), 4)

    def test_declining_and_eof_leave_project_unchanged(self):
        for answers in ('1\nn\n', '1\n\n', '\x04'):
            code, output = self.run_installer(answers)
            self.assertEqual(code, 0, output)
            self.assertEqual(list(self.project.iterdir()), [])

    def test_multiple_choices_deduplicate_shared_paths(self):
        code, output = self.run_installer('1,2,3,1\ny\n')
        self.assertEqual(code, 0, output)
        self.assertEqual(output.count('Installed:'), 2)
        self.assert_complete(self.project / '.agents/skills/albanian-humanizer')
        self.assert_complete(self.project / '.claude/skills/albanian-humanizer')

    def test_custom_path_with_spaces_and_shell_characters_is_literal(self):
        folder = self.project / 'my skills $(touch nope)'
        code, output = self.run_installer(f'0\n{folder}\ny\n')
        self.assertEqual(code, 0, output)
        self.assert_complete(folder / 'albanian-humanizer')
        self.assertFalse((self.project / 'nope').exists())

    def test_update_preserves_old_copy_in_backup(self):
        destination = self.project / '.claude/skills/albanian-humanizer'
        destination.mkdir(parents=True)
        (destination / 'personal.txt').write_text('keep my edit')
        code, output = self.run_installer('2\ny\n')
        self.assertEqual(code, 0, output)
        self.assert_complete(destination)
        backups = list(destination.parent.glob('.albanian-humanizer-backup.*/albanian-humanizer/personal.txt'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), 'keep my edit')

    def test_symlink_destination_is_not_followed(self):
        parent = self.project / '.claude/skills'
        parent.mkdir(parents=True)
        other = self.project / 'other'
        other.mkdir()
        (parent / 'albanian-humanizer').symlink_to(other, target_is_directory=True)
        code, output = self.run_installer('2\ny\n')
        self.assertNotEqual(code, 0, output)
        self.assertEqual(list(other.iterdir()), [])

    def test_all_profiles_install_complete_copies(self):
        code, output = self.run_installer('all\ny\n')
        self.assertEqual(code, 0, output)
        folders = {line.split('|')[2] for line in (ROOT / 'installer/agents.txt').read_text().splitlines()}
        for folder in folders:
            self.assert_complete(self.project / folder / 'albanian-humanizer')
        self.assertEqual(output.count('Installed:'), len(folders))

    def test_dry_run_does_not_create_destinations(self):
        code, output = self.run_installer('1\n', extra=['--dry-run'])
        self.assertEqual(code, 0, output)
        self.assertIn('Dry run:', output)
        self.assertEqual(list(self.project.iterdir()), [])

    def test_missing_source_and_failed_download_do_not_install(self):
        code, output = self.run_installer('', extra=['--source', str(self.project)])
        self.assertNotEqual(code, 0, output)
        fake = self.project / 'bin'
        fake.mkdir()
        curl = fake / 'curl'
        curl.write_text('#!/bin/sh\nexit 22\n')
        curl.chmod(0o755)
        env = dict(os.environ, PATH=f'{fake}{os.pathsep}{os.environ["PATH"]}', TMPDIR=str(self.project))
        command = ['bash', '-o', 'pipefail', '-c', 'cat "$1" | bash', '_', str(ROOT / 'install.sh')]
        code, output = self.run_installer('', command=command, env=env)
        self.assertNotEqual(code, 0, output)
        self.assertIn('Cannot download', output)
        self.assertEqual(list(self.project.iterdir()), [fake])


if __name__ == '__main__':
    unittest.main()
