

use std::io;
use rand::Rng;
use std::cmp::Ordering;

fn main() {
  println!("Guess the number");
  
  let secret_number = rand::thread_rng().gen_range(1..=100);// generate a random number in range 1-100
  println!("Secret number: {}",secret_number);


  loop{
    println!("Enter your guess: "); // guess is a string not a int
    let mut guess = String::new();
  
  
    io::stdin().read_line(&mut guess).expect("Can't read your input");
  
    // Create a shadow means we can reuse name of existed variable
  
    //trim() -> eliminate any whitespace at the beginning and the end
  
    // parse() -> convert a string to another type, if it successfully converts from string to number, returns Ok
    // otherwise, return Err


    let guess: u32 = guess.trim().parse(){
        Ok(num) => num,
        Err(_) => continue,
    };
  
    println!("Your guess number: {}",guess);
  
  
    match guess.cmp(&secret_number) {
      Ordering::Less => println!("Too small!"),
      Ordering::Greater => println!("Too big!"),
      Ordering::Equal => {
        println!("You win!");
        break;
      }
  }
  

  }
}
