from src.basico import soma, media, eh_palindromo


def test_soma():
    assert soma(2, 3) == 5
    assert soma(-1, 1) == 0


def test_media():
    assert media([1, 2, 3]) == 2
    assert media([10, 0]) == 5


def test_eh_palindromo():
    assert eh_palindromo("arara")
    assert eh_palindromo("Ame a ema")
    assert not eh_palindromo("python")
