use std::{fs, u32};

fn main() {
    part_1();
    part_2();
}

fn part_1() {
    let contents = fs::read_to_string("../input.txt").unwrap();
    let lines: Vec<_> = contents.split("\n").collect();
    let mut nums = vec![];
    for i in 0..lines.len() {
        let mut num_bucket = vec![];
        for j in 0..lines[i].len() {
            let c = lines[i].chars().nth(j).unwrap();
            let next_c = lines[i].chars().nth(j + 1);
            if c.is_numeric() {
                num_bucket.push(c);
            }
            if let Some(next_c) = next_c {
                if next_c.is_numeric() {
                    continue;
                }
            }

            if num_bucket.len() < 1 {
                continue;
            }

            let raw_num: String = num_bucket.iter().collect();
            let parsed_num: u32 = raw_num.parse().unwrap();
            let bounding_box = (
                (i.saturating_sub(1), j.saturating_sub(num_bucket.len())),
                (i + 1, j + 1),
            );
            if is_part_num(&lines, bounding_box) {
                nums.push(parsed_num)
            }
            num_bucket.clear();
        }
    }
    println!("{}", nums.iter().sum::<u32>());
}

fn is_part_num(lines: &Vec<&str>, bounding_box: ((usize, usize), (usize, usize))) -> bool {
    for i in bounding_box.0 .0..=bounding_box.1 .0 {
        if let Some(row) = lines.get(i) {
            for j in bounding_box.0 .1..=bounding_box.1 .1 {
                if let Some(ch) = row.chars().nth(j) {
                    if !(ch.is_digit(10) || ch.eq(&'.')) {
                        return true;
                    }
                }
            }
        }
    }
    false
}

fn find_num(line: &str, pos: usize) -> Option<(u32, usize)> {
    let ch_root = line.chars().nth(pos).unwrap_or('.');

    if !ch_root.is_numeric() {
        return None;
    }

    let mut ch_prefix_bucket = vec![ch_root];

    let mut i = pos;
    while i > 0 && pos > 0 {
        i -= 1;
        if let Some(c) = line.chars().nth(i) {
            if c.is_numeric() {
                ch_prefix_bucket.push(c);
            } else {
                break;
            }
        }
    }

    let mut ch_suffix_bucket = vec![];

    let mut i = pos + 1;
    while i < line.len() {
        if let Some(c) = line.chars().nth(i) {
            if c.is_numeric() {
                ch_suffix_bucket.push(c);
            } else {
                break;
            }
        }
        i += 1;
    }

    let num: u32 = ch_prefix_bucket
        .iter()
        .rev()
        .chain(&ch_suffix_bucket)
        .collect::<String>()
        .parse()
        .unwrap();

    Some((num, ch_suffix_bucket.len()))
}

fn gear_ratio(lines: &Vec<&str>, bounding_box: ((usize, usize), (usize, usize))) -> u32 {
    let mut nums = vec![];
    for i in bounding_box.0 .0..=bounding_box.1 .0 {
        if let Some(row) = lines.get(i) {
            let mut j = bounding_box.0 .1;
            while j <= bounding_box.1 .1 {
                let mut skip = 1;
                if let Some(_) = row.chars().nth(j) {
                    if let Some((num, s)) = find_num(row, j) {
                        nums.push(num);
                        skip += s;
                    }
                }
                j += skip;
            }
        }
    }
    if nums.len() == 2 {
        nums.iter().product()
    } else {
        0
    }
}

fn part_2() {
    let contents = fs::read_to_string("../input.txt").unwrap();
    let lines: Vec<_> = contents.split("\n").collect();
    let mut nums = vec![];
    for i in 0..lines.len() {
        for j in 0..lines[i].len() {
            let c = lines[i].chars().nth(j).unwrap();
            if c != '*' {
                continue;
            }

            let bounding_box = ((i.saturating_sub(1), j.saturating_sub(1)), (i + 1, j + 1));
            nums.push(gear_ratio(&lines, bounding_box));
        }
    }
    println!("{}", nums.iter().sum::<u32>());
}
