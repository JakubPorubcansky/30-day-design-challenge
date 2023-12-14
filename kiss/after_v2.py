def count_fruits(fruits: list[str]) -> dict[str, int]:
    fruits_dict: dict[str, int] = {}
    for fruit in fruits:
        if fruit in fruits_dict:
            fruits_dict[fruit] += 1
        else:
            fruits_dict[fruit] = 1
    return fruits_dict


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
