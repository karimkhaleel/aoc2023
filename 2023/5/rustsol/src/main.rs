use std::fs;

#[derive(Debug)]
struct Bucket {
    start: i64,
    end: i64,
    diff: i64,
}

impl Bucket {
    fn map(&self, src: i64) -> i64 {
        if src >= self.start && src < self.end {
            src + self.diff
        } else {
            src
        }
    }
}

#[derive(Debug)]
struct DSMap {
    buckets: Vec<Bucket>,
}

impl DSMap {
    fn map(&self, src: i64) -> i64 {
        match self.buckets.binary_search_by(|n| n.start.cmp(&src)) {
            Ok(i) => self.buckets.get(i).unwrap().map(src),
            Err(i) => self.buckets.get(i.saturating_sub(1)).unwrap().map(src),
        }
    }
}

fn main() {
    let content = fs::read_to_string("../input.txt").unwrap();
    let mut lines_iter = content.split("\n").filter(|&l| l != "");
    let seeds = parse_nums(lines_iter.next().unwrap());
    let mut maps = vec![];
    for line in lines_iter {
        let nums = parse_nums(&line);
        // Encountered a new mapping
        if nums.len() == 0 {
            maps.push(DSMap { buckets: vec![] });
        }
        if let [dest, src, interval] = nums[..] {
            maps.last_mut().unwrap().buckets.push(Bucket {
                start: src,
                end: src + interval,
                diff: dest - src,
            });
        }
    }
    maps.iter_mut()
        .for_each(|m| m.buckets.sort_unstable_by(|a, b| a.start.cmp(&b.start)));
    let result_vec: Vec<_> = seeds
        .iter()
        .map(|s| maps.iter().fold(*s, |acc, item| item.map(acc)))
        .collect();
    let result = result_vec.iter().min().unwrap();

    println!("Part 1: {result:?}");

    let mut part_two_result = vec![];
    seeds.chunks(2).for_each(|chunk| {
        println!("{:?}", chunk[0]..(chunk[0] + chunk[1]));
        (chunk[0]..(chunk[0] + chunk[1]))
            .for_each(|s| part_two_result.push(maps.iter().fold(s, |acc, item| item.map(acc))))
    });
    let result = part_two_result.iter().min().unwrap();
    println!("Part 2: {result:?}");
}

fn parse_nums(line: &str) -> Vec<i64> {
    line.split(" ").filter_map(|n| n.parse().ok()).collect()
}
