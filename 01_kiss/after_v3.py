from collections import Counter


def count_fruits(fruits: list[str]) -> dict[str, int]:
    return Counter(fruits)


def main() -> None:
    assert count_fruits(
        [
            "apple",
            "banana",
            "apple",
            "cherry",
            "banana",
            "cherry",
            "apple",
            "apple",
            "cherry",
            "banana",
            "cherry",
        ]
    ) == {"apple": 4, "banana": 3, "cherry": 4}
    assert count_fruits([]) == {}
    assert count_fruits(["apple", "apple", "apple", "apple"]) == {"apple": 4}
    assert count_fruits(["banana"]) == {"banana": 1}


if __name__ == "__main__":
    main()
