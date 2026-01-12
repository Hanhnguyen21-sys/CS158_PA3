// make some changes
/*

Ownership rules: 
1. each value has a variable that's its owner
2. can be only one owner at a time
3. when owner go out of scope, value will be dropped

*/

fn main()
{
    let s1 = String::from("Rust Example"); //s1 is owner of "Rust Example" string
    // if we pass the ownership from s1 to s2
    // now, only s2 own the string "Rust Example"
    let s2= s1;
    // we can't do println!("{}",s1);
    println!("{}",s2);
    let len = get_length(&s2);
    println!("Length of string: {}",len);
}

fn get_length(s:&String) -> usize{
    s.len()
}