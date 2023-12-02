use regex::Regex;

pub fn process_part_1_line(line: &str, game_re: &Regex, sample_re: &Regex) -> Option<u32> {
    let caps = game_re.captures(line)?;
    let game = caps.get(1)?.as_str();
    let samples = caps.get(2)?.as_str();

    samples
        .split(';')
        .all(|sample_data| {
            sample_data.split(',').all(|color_data| {
                if let Some(caps) = sample_re.captures(color_data) {
                    let number: u32 = match caps.get(1) {
                        Some(cap) => match cap.as_str().parse() {
                            Ok(num) => num,
                            Err(_) => return false,
                        },
                        None => return false,
                    };
                    match caps.get(2) {
                        Some(cap) => match cap.as_str() {
                            "red" => number <= 12,
                            "green" => number <= 13,
                            "blue" => number <= 14,
                            _ => false,
                        },
                        None => false,
                    }
                } else {
                    false
                }
            })
        })
        .then(|| game.parse().ok())
        .flatten()
}

struct MinColors {
    r: u32,
    g: u32,
    b: u32,
}

impl MinColors {
    fn power(&self) -> u32 {
        self.r * self.g * self.b
    }
}

pub fn process_part_2_line(line: &str, game_re: &Regex, sample_re: &Regex) -> Option<u32> {
    let caps = game_re.captures(line)?;
    let samples = caps.get(2)?.as_str();

    let mut min_colors = MinColors { r: 1, g: 1, b: 1 };

    let _ = samples.split(';').for_each(|sample_data| {
        sample_data.split(',').for_each(|color_data| {
            if let Some(caps) = sample_re.captures(color_data) {
                let number: u32 = match caps.get(1) {
                    Some(cap) => match cap.as_str().parse() {
                        Ok(num) => num,
                        Err(_) => 1,
                    },
                    None => 1,
                };
                match caps.get(2) {
                    Some(cap) => match cap.as_str() {
                        "red" => {
                            if min_colors.r < number {
                                min_colors.r = number
                            }
                        }
                        "green" => {
                            if min_colors.g < number {
                                min_colors.g = number
                            }
                        }
                        "blue" => {
                            if min_colors.b < number {
                                min_colors.b = number
                            }
                        }
                        _ => (),
                    },
                    None => (),
                }
            }
        })
    });

    Some(min_colors.power())
}
