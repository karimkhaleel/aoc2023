use std::fs;

// fn main() {
//     let contents = fs::read_to_string("../input.txt").unwrap();
//     let mut sum = 0;
//     for line in contents.split("\n") {
//         println!("{line}");
//         let mut first_number = 0;
//         let mut last_number = 0;
//         let mut first_number_set = false;
//         for ch in line.chars() {
//             if !first_number_set && ch.is_numeric() {
//                 if let Some(digit) = ch.to_digit(10) {
//                     first_number = digit;
//                     last_number = digit;
//                     first_number_set = true;
//                 }
//             } else if ch.is_numeric() {
//                 if let Some(digit) = ch.to_digit(10) {
//                     last_number = digit;
//                 }
//             }
//         }
//         sum += first_number * 10 + last_number;
//     }
//
//     println!("{sum}");
// }

fn main() {
    // let sum = fs::read_to_string("../input.txt")
    //     .unwrap()
    //     .lines()
    //     .filter_map(|line| process_1_line(line))
    //     .sum::<u32>();
    //
    // println!("{sum}");

    let sum = fs::read_to_string("../input.txt")
        .unwrap()
        .lines()
        .filter_map(|line| process_2_line(line))
        .sum::<u32>();

    println!("{sum}");
}

fn process_1_line(line: &str) -> Option<u32> {
    let digits: Vec<u32> = line.chars().filter_map(|ch| ch.to_digit(10)).collect();

    match (digits.first(), digits.last()) {
        (Some(&first), Some(&last)) => Some(first * 10 + last),
        _ => None,
    }
}

fn process_2_line(line: &str) -> Option<u32> {
    let mut digits = vec![];
    let mut acc = String::new();
    for c in line.chars() {
        if let Some(d) = c.to_digit(10) {
            digits.push(d);
            // acc.clear();
        } else {
            acc.push(c);
            if let Some(digit) = match acc {
                _ if acc.ends_with("one") => Some(1),
                _ if acc.ends_with("two") => Some(2),
                _ if acc.ends_with("three") => Some(3),
                _ if acc.ends_with("four") => Some(4),
                _ if acc.ends_with("five") => Some(5),
                _ if acc.ends_with("six") => Some(6),
                _ if acc.ends_with("seven") => Some(7),
                _ if acc.ends_with("eight") => Some(8),
                _ if acc.ends_with("nine") => Some(9),
                _ => None,
            } {
                digits.push(digit);
                // acc.clear();
            }
        }
    }

    match (digits.first(), digits.last()) {
        (Some(&first), Some(&last)) => Some(first * 10 + last),
        _ => None,
    }
}
