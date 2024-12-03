use std::fs;

fn main() {
    let content = fs::read_to_string("../test_3.txt").unwrap();
    let map: Vec<Vec<_>> = content
        .split("\n")
        .filter(|line| line.len() > 0)
        .map(|line| line.chars().collect())
        .collect();

    let longest = rustsol::find_longest_path(&map);
    print!("{longest}\n");
    let largest = rustsol::find_enclosed_tiles(&map);
    print!("{largest}\n");
}
