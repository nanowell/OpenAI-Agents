use std::collections::HashMap;

fn main() {
    let mut map = HashMap::new();
    for (y, line) in vec![
        "##..##..",
        ".##.####",
        "##.#..##",
        "##..#..#",
        "###.#.#.",
        "##..#..#",
        "#.#..#.#",
        ".##.####",
    ].into_iter().enumerate() {
        for (x, c) in line.chars().enumerate() {
            map.insert((x, y), c);
        }
    }

    let mut x = 0;
    let mut y = 0;
    let mut direction = 0;
    let mut infected = 0;
    for _ in 0..10000000 {
        let current = *map.entry((x, y)).or_insert('.');
        match current {
            '.' => {
                direction = (direction + 3) % 4;
                map.insert((x, y), 'W');
            }
            'W' => {
                map.insert((x, y), '#');
                infected += 1;
            }
            '#' => {
                direction = (direction + 1) % 4;
                map.insert((x, y), 'F');
            }
            'F' => {
                direction = (direction + 2) % 4;
                map.insert((x, y), '.');
            }
            _ => panic!("Unexpected char: {}", current),
        }

        match direction {
            0 => y = y.saturating_sub(1),
            1 => x = x.saturating_add(1),
            2 => y = y.saturating_add(1),
            3 => x = x.saturating_sub(1),
            _ => panic!("Unexpected direction: {}", direction),
        }
        print!("\x1Bc");
        for y in 0..map.keys().map(|k| k.1).max().unwrap() + 1 {
            for x in 0..map.keys().map(|k| k.0).max().unwrap() + 1 {
                let c = *map.entry((x, y)).or_insert('.');
                print!("{}", c);
            }
            println!("");
        }
        std::thread::sleep(std::time::Duration::from_millis(100));
    }

    println!("Infected: {}", infected);
}

