def soma_dos_quadrados(numeros: list[int]) -> int:
    """
    Exemplo para praticar com GitHub Copilot.

    Ideia:
    - Deixe apenas assinatura + docstring.
    - Peça ao Copilot sugerir a implementação.

    A função deve retornar a soma dos quadrados de cada número da lista.
    """
    return sum(n * n for n in numeros)


def dividir(a: int, b: int) -> float:
    """
    Função com BUG proposital para praticar Copilot Chat.

    Teste no console:
    - dividir(10, 0)

    Depois peça ao Copilot:
    "Explique o erro e sugira uma correção tratando divisão por zero."
    """
    return a / b  # bug proposital
