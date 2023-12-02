use regex::Regex;
use sol::{process_part_1_line, process_part_2_line};
use std::{fs, u32};

// fn main() {
//     let sum = fs::read_to_string("../input.txt")
//         .unwrap()
//         .lines()
//         .filter_map(|line| process_line(line))
//         .sum::<u32>();
//
//     println!("{sum}");
// }
//
// fn process_line(line: &str) -> Option<u32> {
//     let game_re = RegexBuilder::new(r"Game (\d+):(.*)").build().unwrap();
//     let sample_re = RegexBuilder::new(r"(\d+) (.*)").build().unwrap();
//
//     let (_, [game, samples]) = game_re.captures(line).unwrap().extract();
//     for sample_data in samples.split(";") {
//         for color_data in sample_data.split(",") {
//             if !match sample_re.captures(color_data).unwrap().extract() {
//                 (_, [number, "red"]) => is_possible(number, "red"),
//                 (_, [number, "green"]) => is_possible(number, "green"),
//                 (_, [number, "blue"]) => is_possible(number, "blue"),
//                 _ => false,
//             } {
//                 return None;
//             }
//         }
//     }
//     let game_id: u32 = game.parse().unwrap();
//     Some(game_id)
// }
//
// fn is_possible(raw_number: &str, color: &str) -> bool {
//     let number: u32 = raw_number.parse().unwrap();
//     match color {
//         "red" => number <= 12,
//         "green" => number <= 13,
//         "blue" => number <= 14,
//         _ => false,
//     }
// }

// Part 1
fn main() {
    let game_re = Regex::new(r"Game (\d+):(.*)").unwrap();
    let sample_re = Regex::new(r"(\d+) (.*)").unwrap();

    let sum_part_1 = fs::read_to_string("../input.txt")
        .expect("Failed to read file")
        .lines()
        .filter_map(|line| process_part_1_line(line, &game_re, &sample_re))
        .sum::<u32>();

    println!("{sum_part_1}");

    let sum_part_2 = fs::read_to_string("../input.txt")
        .expect("Failed to read file")
        .lines()
        .filter_map(|line| process_part_2_line(line, &game_re, &sample_re))
        .sum::<u32>();

    println!("{sum_part_2}");
}
