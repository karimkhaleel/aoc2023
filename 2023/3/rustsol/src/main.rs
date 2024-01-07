use std::fs;

fn main() {
    let binding = fs::read_to_string("../input-test.txt").unwrap();
    let lines = binding.split("\n").collect();
    let result = rustsol::parse(&lines);
    print!("{result}")
}
