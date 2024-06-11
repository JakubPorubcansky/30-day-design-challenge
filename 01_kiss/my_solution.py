def count_fruits(fruits: list[str]) -> dict[str, int]:
    d = {}

    for fruit in fruits:
        if fruit:
            fruit_norm = fruit.lower().strip()
            d[fruit_norm] = d.get(fruit_norm, 0) + 1
    
    return d


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
    assert count_fruits(["", "", "apple", "APplE", "    appLe "]) == {"apple": 3}

    print("Success!")


if __name__ == "__main__":
    main()
