use std::collections::HashMap;

fn print_grid(map: &HashMap<(i32, i32), char>) {
    let max_x = map.keys().map(|k| k.0).max().unwrap_or(0);
    let max_y = map.keys().map(|k| k.1).max().unwrap_or(0);

    for y in 0..=max_y {
        for x in 0..=max_x {
            let c = *map.get(&(x, y)).unwrap_or(&'.');
            print!("{}", c);
        }
        println!("");
    }
    println!("");
}

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
            map.insert((x as i32, y as i32), c);
        }
    }

    let mut x = 0;
    let mut y = 0;
    let mut direction = 0;
    let mut infected = 0;

    let mut actions = HashMap::new();
    actions.insert('.', (3, 'W'));
    actions.insert('W', (0, '#'));
    actions.insert('#', (1, 'F'));
    actions.insert('F', (2, '.'));

    for _ in 0..10000000 {
        let current = *map.entry((x, y)).or_insert('.');
        let (turn, new_state) = actions.get(&current).unwrap();
        direction = (direction + turn) % 4;
        map.insert((x, y), *new_state);
        if *new_state == '#' {
            infected += 1;
        }

        match direction {
            0 => y -= 1,
            1 => x += 1,
            2 => y += 1,
            3 => x -= 1,
            _ => panic!("Unexpected direction: {}", direction),
        }

        print_grid(&map);
    }

    println!("Infected: {}", infected);
}
