use num_integer::lcm;
use std::{collections::HashMap, fs};

fn main() {
    let content = fs::read_to_string("../input.txt").unwrap();
    let mut lines = content.split("\n");
    let directions = lines.nth(0).unwrap();

    fn parse(l: &str) -> Option<(String, (String, String))> {
        let mut parts = l.split(" = ");
        let start = parts.next()?;
        let destinations: Vec<_> = parts
            .next()?
            .trim_start_matches('(')
            .trim_end_matches(')')
            .split(", ")
            .collect();

        if destinations.len() != 2 {
            None
        } else {
            Some((
                start.to_string(),
                (destinations[0].to_string(), destinations[1].to_string()),
            ))
        }
    }

    let nodes: HashMap<String, (String, String)> = lines.filter_map(parse).collect();

    part1(&nodes, directions);
    part2(&nodes, directions);
}

fn part1(nodes: &HashMap<String, (String, String)>, directions: &str) {
    let mut count = 0;

    let mut location = &String::from("AAA");
    let end = &String::from("ZZZ");

    let _ = directions.chars().cycle().try_for_each(|d| {
        if location == end {
            Err("Done")
        } else {
            location = match d {
                'L' => &nodes[location].0,
                'R' => &nodes[location].1,
                _ => panic!(),
            };
            count += 1;
            Ok(())
        }
    });

    println!("{count}");
}

fn part2(nodes: &HashMap<String, (String, String)>, directions: &str) {
    let locations: Vec<_> = nodes.keys().filter(|k| k.ends_with('A')).collect();

    let end_counts = locations.iter().map(|loc| {
        let mut l = &String::from(*loc);
        let mut count = 0;
        for c in directions.chars().cycle() {
            if l.ends_with("Z") {
                break;
            }

            l = match c {
                'L' => &nodes[&l[..]].0,
                'R' => &nodes[&l[..]].1,
                _ => panic!(),
            };

            count += 1;
        }
        count as i64
    });

    let steps = end_counts.reduce(lcm).unwrap();

    println!("{steps}");
}
