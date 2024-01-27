use std::fs;

fn main() {
    let content = fs::read_to_string("../input.txt").unwrap();
    let result = content.split("\n").filter(|l| l.len() > 0).map(|l| {
        l.split(" ")
            .filter_map(|n| n.parse::<i32>().ok())
            .collect::<Vec<_>>()
    });

    let result_1: i32 = result
        .clone()
        .map(|n| extrapolate(&n, n.last().unwrap()))
        .sum();
    let result_2: i32 = result.clone().map(|n| extrapolate_history(&n)).sum();

    println!("{result_1}");
    println!("{result_2}");
}

fn extrapolate(nums: &Vec<i32>, last: &i32) -> i32 {
    if nums.iter().max().unwrap() == nums.iter().min().unwrap() {
        return *last;
    } else {
        let diffs = nums.windows(2).map(|w| w[1] - w[0]).collect::<Vec<_>>();
        return extrapolate(&diffs, &(last + diffs.last().unwrap()));
    }
}

fn extrapolate_history(nums: &Vec<i32>) -> i32 {
    if nums.iter().max().unwrap() == nums.iter().min().unwrap() {
        return *nums.first().unwrap();
    } else {
        let diffs = nums.windows(2).map(|w| w[1] - w[0]).collect::<Vec<_>>();
        let diff = nums.first().unwrap() - extrapolate_history(&diffs);
        return diff;
    }
}
