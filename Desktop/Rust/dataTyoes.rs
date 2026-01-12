
//Lecture about Data Types

// Compound Data Types
// arrays, tuples, slices and strings



fn main(){

    // ARRAYS
    // declare size and type of the array
    let numbers: [i32; 5]= [1,2,3,4,5];

    println!("Array: {:?}",numbers);
    
    let fruits: [&str;3] = ["Apple", "Banana","Grape"];
    println!("Fruits Array: {:?}",fruits);


    //=========================================
    //TUPLES

    let human: (String,i32, bool) = ("Nguyen".to_string(),23,true);
    println!("Person tuple: {:?}", human);

    let my_mix = ("Name",32,true,[1,2,3]);
    println!("My mix tuple: {:?}",my_mix);
    //=========================================
    // SLICES: [1,2,3,5,6]

    let num_slices:&[i32] = &[1,2,3,4,5,6];
    println!("My slices :{:?}", num_slices);

    let animal: &[&str] = &["Dog","Cat","Elephant"];
    println!("Animal Slices :{:?}",animal);

    let subject_slices: &[&String] = &[&"Math".to_string(),&"Physics".to_string(),&"Chem".to_string()];
    println!("Subjects Slices :{:?}",subject_slices);
    

    // Strings [growable, mutable, owned string type]  , is allocated in heap -> grow dynamically
    // String slices (&str): stored in stack, & indicates memory address, quicker but can't be mutable
    let mut example: String = String::from("Hell, "); //key word mut allows users modify that string
    // adding more to the string
    example.push_str("Yeah!");
    println!("Example says: {}",example);


    //&str
    let string: String = String::from("Hello, World");
    let slice: &str = &string[0..5]; // slice variable now has value stored in string
    println!("Slice: {}",slice);


}