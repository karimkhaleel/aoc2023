use std::{collections::HashSet, fs, vec};

fn main() {
    let content = fs::read_to_string("../input.txt").unwrap();
    let lines: Vec<_> = content.lines().collect();
    let base: u32 = 2;
    let mut scores = vec![];
    let mut wins = vec![0; lines.len()];
    for (i, line) in lines.iter().enumerate() {
        let start_winning = line.find(": ").unwrap() + 1;
        let end_winning = line.find(" |").unwrap();
        let start_mine = line.find("| ").unwrap() + 2;
        let winning = get_numbers(&line[start_winning..end_winning]);
        let winning_set: HashSet<u32> = HashSet::from_iter(winning.clone());
        let mine = get_numbers(&line[start_mine..]);
        let power = mine
            .iter()
            .filter(|n| winning_set.contains(n))
            .collect::<Vec<_>>()
            .len() as u32;
        let mut score = 0;
        if power > 0 {
            score = base.pow(power.saturating_sub(1));
        }
        scores.push(score);
        wins[i] += 1;
        let current_wins = wins[i];
        for j in i + 1..=i + power as usize {
            wins[j] += 1 * current_wins;
        }
    }

    println!("Part 1: {}", scores.iter().sum::<u32>());
    println!("Part 2: {:?}", wins.iter().sum::<u32>());
}

fn get_numbers(line: &str) -> Vec<u32> {
    line.split(' ')
        .filter_map(|n| n.parse::<u32>().ok())
        .collect()
}
