"""Utility functions for electronic configuration and valence analysis."""


def calculate_chemistry_data(atomic_number):
    """Return the electronic configuration, valence electrons, and octet holes."""
    if not isinstance(atomic_number, int) or atomic_number < 1:
        return None

    orbitals_order = [
        (1, 0, 2, "1s"), (2, 0, 2, "2s"), (2, 1, 6, "2p"), (3, 0, 2, "3s"),
        (3, 1, 6, "3p"), (4, 0, 2, "4s"), (3, 2, 10, "3d"), (4, 1, 6, "4p"),
        (5, 0, 2, "5s"), (4, 2, 10, "4d"), (5, 1, 6, "5p"), (6, 0, 2, "6s"),
        (4, 3, 14, "4f"), (5, 2, 10, "5d"), (6, 1, 6, "6p"), (7, 0, 2, "7s"),
        (5, 3, 14, "5f"), (6, 2, 10, "6d"), (7, 1, 6, "7p"),
    ]

    remaining_electrons = atomic_number
    config_parts = []
    shell_electrons = []
    max_n = 0

    for n, _l, cap, label in orbitals_order:
        if remaining_electrons <= 0:
            break

        electrons_in_orbital = min(remaining_electrons, cap)
        config_parts.append(f"{label}^{electrons_in_orbital}")
        shell_electrons.append({"n": n, "e": electrons_in_orbital})
        max_n = max(max_n, n)
        remaining_electrons -= electrons_in_orbital

    valence_electrons = sum(orbital["e"] for orbital in shell_electrons if orbital["n"] == max_n)
    target_valence = 2 if max_n == 1 else 8
    holes = max(target_valence - valence_electrons, 0)

    return {
        "configuration": " ".join(config_parts),
        "valence": valence_electrons,
        "holes": holes,
    }
