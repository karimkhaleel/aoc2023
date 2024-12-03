use std::{collections::HashSet, fmt::Debug, usize};

type Coordinates = (usize, usize);

struct Node<'a> {
    symbol: char,
    coordinates: Coordinates,
    fits: String,
    prev: Option<&'a Node<'a>>,
    map: &'a Vec<Vec<char>>,
}

impl Debug for Node<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("Node")
            .field("symbol", &self.symbol)
            .field("coordinates", &self.coordinates)
            .field("fits", &self.fits)
            .finish()
    }
}

impl Node<'_> {
    fn fits_up(&self, other: &Self) -> bool {
        match self.symbol {
            'S' => other.symbol != '.',
            '|' | 'L' | 'J' => match other.symbol {
                '|' | '7' | 'F' | 'S' => true,
                _ => false,
            },
            _ => false,
        }
    }

    fn fits_down(&self, other: &Self) -> bool {
        match self.symbol {
            'S' => other.symbol != '.',
            '|' | '7' | 'F' => match other.symbol {
                '|' | 'L' | 'J' | 'S' => true,
                _ => false,
            },
            _ => false,
        }
    }

    fn fits_left(&self, other: &Self) -> bool {
        match self.symbol {
            'S' => other.symbol != '.',
            '-' | '7' | 'J' => match other.symbol {
                '-' | 'L' | 'F' | 'S' => true,
                _ => false,
            },
            _ => false,
        }
    }

    fn fits_right(&self, other: &Self) -> bool {
        match self.symbol {
            'S' => other.symbol != '.',
            '-' | 'L' | 'F' => match other.symbol {
                '-' | '7' | 'J' | 'S' => true,
                _ => false,
            },
            _ => false,
        }
    }

    fn get_next_node(&self) -> Option<Node> {
        let (x, y) = self.coordinates;
        // UP
        let up_y = y.checked_sub(1);
        let up_x = x;
        if let Some(up_y) = up_y {
            let candidate = Node {
                symbol: self.map[up_y][up_x],
                coordinates: (up_x, up_y),
                fits: String::from("UP"),
                prev: Some(self),
                map: self.map,
            };
            if self.fits_up(&candidate) {
                match self.prev {
                    Some(n) if n.coordinates == candidate.coordinates => {}
                    _ => return Some(candidate),
                }
            }
        }
        // DOWN
        let down_y = y + 1;
        let down_x = x;
        if down_y < self.map.len() {
            let candidate = Node {
                symbol: self.map[down_y][down_x],
                coordinates: (down_x, down_y),
                fits: String::from("DOWN"),
                prev: Some(self),
                map: self.map,
            };
            if self.fits_down(&candidate) {
                match self.prev {
                    Some(n) if n.coordinates == candidate.coordinates => {}
                    _ => return Some(candidate),
                }
            }
        }
        // LEFT
        let left_x = x.checked_sub(1);
        let left_y = y;
        if let Some(left_x) = left_x {
            let candidate = Node {
                symbol: self.map[left_y][left_x],
                coordinates: (left_x, left_y),
                fits: String::from("LEFT"),
                prev: Some(self),
                map: self.map,
            };
            if self.fits_left(&candidate) {
                match self.prev {
                    Some(n) if n.coordinates == candidate.coordinates => {}
                    _ => return Some(candidate),
                }
            }
        }
        // RIGHT
        let right_y = y;
        let right_x = x + 1;
        if right_x < self.map.first().unwrap().len() {
            let candidate = Node {
                symbol: self.map[right_y][right_x],
                coordinates: (right_x, right_y),
                fits: String::from("RIGHT"),
                prev: Some(self),
                map: self.map,
            };
            if self.fits_right(&candidate) {
                match self.prev {
                    Some(n) if n.coordinates == candidate.coordinates => {}
                    _ => return Some(candidate),
                }
            }
        }
        return None;
    }
}

pub fn find_longest_path(map: &Vec<Vec<char>>) -> usize {
    let n = find_start_node(&map).unwrap();
    let mut seen = HashSet::new();
    seen.insert(n.coordinates);
    let mut path = Vec::new();
    path.push(n.coordinates);
    trace(&n, 1, &mut seen, &mut path) / 2
}

pub fn find_enclosed_tiles(map: &Vec<Vec<char>>) -> usize {
    let n = find_start_node(&map).unwrap();
    let mut seen = HashSet::new();
    seen.insert(n.coordinates);
    let mut path = Vec::new();
    path.push(n.coordinates);
    trace(&n, 1, &mut seen, &mut path);
    for i in 0..map.len() {
        for y in 0..map.first().unwrap().len() {
            if seen.contains(&(y, i)) {
                print!("O");
            } else {
                let val = map[i][y];
                print!("{val}");
            }
        }
        println!();
    }

    path.iter().for_each(|n| println!("{n:?}"));

    0
}

fn trace(
    node: &Node,
    depth: usize,
    seen: &mut HashSet<Coordinates>,
    path: &mut Vec<Coordinates>,
) -> usize {
    if let Some(neighbor) = node.get_next_node() {
        if seen.insert(neighbor.coordinates) {
            path.push(neighbor.coordinates);
            return trace(&neighbor, depth + 1, seen, path);
        }
    }
    depth
}

fn find_start_node(map: &Vec<Vec<char>>) -> Option<Node> {
    if let Some(c) = map.iter().flatten().position(|&x| x == 'S') {
        let coordinates = (c / map.len(), c % map.len());
        return Some(Node {
            symbol: 'S',
            coordinates,
            fits: "".to_string(),
            prev: None,
            map,
        });
    }
    None
}
