import os
import pytest

from app.evaluations import evaluate


class TestShellCommands:
    # Echo command tests
    def test_echo_basic(self, capsys):
        evaluate("echo hello world")
        captured = capsys.readouterr()
        assert captured.out == "hello world\n"

    def test_echo_empty(self, capsys):
        evaluate("echo")
        captured = capsys.readouterr()
        assert captured.out == "\n"

    def test_echo_special_chars(self, capsys):
        evaluate("echo hello! @#$% 123")
        captured = capsys.readouterr()
        assert captured.out == "hello! @#$% 123\n"

    # PWD command tests
    def test_pwd(self, capsys):
        evaluate("pwd")
        captured = capsys.readouterr()
        assert captured.out.strip() == os.getcwd()

    # CD command tests
    @pytest.fixture
    def setup_test_dir(self, tmp_path):
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        return test_dir

    def test_cd_valid_dir(self, setup_test_dir):
        original_dir = os.getcwd()
        try:
            evaluate(f"cd {setup_test_dir}")
            assert os.getcwd() == str(setup_test_dir)
        finally:
            os.chdir(original_dir)

    def test_cd_nonexistent_dir(self, capsys):
        evaluate("cd /nonexistent/directory")
        captured = capsys.readouterr()
        assert captured.out == "cd: /nonexistent/directory: No such file or directory"

    def test_cd_to_home(self):
        original_dir = os.getcwd()
        try:
            evaluate("cd ~")
            assert os.getcwd() == os.path.expanduser("~")
        finally:
            os.chdir(original_dir)

    # Type command tests
    def test_type_builtin_command(self, capsys):
        evaluate("type echo")
        captured = capsys.readouterr()
        assert captured.out == "echo is a shell builtin\n"

    def test_type_external_command(self, capsys):
        evaluate("type python")
        captured = capsys.readouterr()
        assert "python is" in captured.out and "python" in captured.out

    def test_type_nonexistent_command(self, capsys):
        evaluate("type nonexistent_command")
        captured = capsys.readouterr()
        assert "not found" in captured.out

    # Exit command tests
    def test_exit_with_valid_code(self):
        with pytest.raises(SystemExit):
            evaluate("exit 0")

    def test_exit_with_invalid_code(self, capsys):
        evaluate("exit invalid")
        captured = capsys.readouterr()
        assert "invalid" in captured.out.lower()

    # Edge cases
    def test_echo_with_quotes(self, capsys):
        evaluate('echo "hello" \'world\'')
        captured = capsys.readouterr()
        assert captured.out == 'hello world\n'

    def test_cd_to_file(self, capsys, tmp_path):
        test_file = tmp_path / "test_file"
        test_file.write_text("")
        evaluate(f"cd {test_file}")
        captured = capsys.readouterr()
        assert "No such file or directory" in captured.out

    # Redirection tests
    def test_output_redirection(self, tmp_path):
        output_file = tmp_path / "out.txt"
        evaluate(f"echo hello world > {output_file}")
        assert output_file.read_text() == "hello world\n"

    def test_output_redirection_with_1(self, tmp_path):
        output_file = tmp_path / "out.txt"
        evaluate(f"echo hello world 1> {output_file}")
        assert output_file.read_text() == "hello world\n"

    def test_error_redirection(self, tmp_path):
        error_file = tmp_path / "err.txt"
        evaluate(f"type nonexistentcommand 2> {error_file}")
        assert "not found" in error_file.read_text()

    def test_redirection_with_external_command(self, tmp_path):
        output_file = tmp_path / "out.txt"
        evaluate(f"python --version > {output_file}")
        assert "Python 3.13.3" in output_file.read_text()

    def test_redirection_overwrites_existing_file(self, tmp_path):
        output_file = tmp_path / "out.txt"
        output_file.write_text("old content")
        evaluate(f"echo new content > {output_file}")
        assert output_file.read_text() == "new content\n"

    def test_redirection_with_special_characters(self, tmp_path):
        output_file = tmp_path / "out.txt"
        evaluate(f"echo 'hello!@#$%^&*()' > {output_file}")
        assert output_file.read_text() == "hello!@#$%^&*()\n"

    def test_empty_output_redirection(self, tmp_path):
        output_file = tmp_path / "out.txt"
        evaluate(f"echo > {output_file}")
        assert output_file.read_text() == "\n"

    def test_multiple_sequential_redirections(self, tmp_path):
        file1 = tmp_path / "out1.txt"
        file2 = tmp_path / "out2.txt"
        evaluate(f"echo first > {file1}")
        evaluate(f"echo second > {file2}")
        assert file1.read_text() == "first\n"
        assert file2.read_text() == "second\n"