use std::fs;

fn main() {
    let content = fs::read_to_string("../input-2.txt").unwrap();
    let inputs = read_input(&content);

    let possible_wins: u64 = inputs
        .iter()
        .map(|pair| {
            let time = pair.0;
            let distance = pair.1;
            (0..=time)
                .map(move |t| t * (time - t))
                .filter(move |r| r > &distance)
                .count() as u64
        })
        .product();

    println!("{possible_wins:?}");
}

fn read_input(content: &str) -> Vec<(u64, u64)> {
    if let [times, distances, _] = content.split("\n").collect::<Vec<_>>().as_slice() {
        let times = times.split(" ").filter_map(|x| x.parse::<u64>().ok());
        let distances = distances.split(" ").filter_map(|x| x.parse::<u64>().ok());
        return times.zip(distances).collect();
    }
    panic!()
}
