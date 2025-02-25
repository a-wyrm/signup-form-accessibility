use std::io;
use std::cmp::Ordering;
use rand::Rng;

fn main() {

    println!("Guess the number!");

    loop { 
        println!("Please input your guess.");
        let secret_number = rand::rng().random_range(1..=100);

        let numb = 1;

        let mut guess = String::new();
        io::stdin()
        .read_line(&mut guess)
        .expect("Failed to read line");
        let guess: u32 = guess.trim().parse().expect("Please type a number!");

        match guess.cmp(&secret_number) {
            Ordering::Greater => println!("Too big!"),
            Ordering::Equal => {println!("You win!"); break},
            Ordering::Less => println!("Too small")

        }

    }
}