
    // create executable file: rustc hello.rs 
    // then run the file: ./hello
    // need to compile file after making changes

    // run by using cargo package
    // cargo new <projectName> 
    // cargo new helloProject
    // create a package 
    // cargo run


    //Primitive data types
    // int,float,boolean, char : are primitive data types

    // Intgers have signed (negative + positive numbers) and unsigned (positive numbers)
    // Ex: i32, i64 (32, 64 indicate the number of bits can be stored in that variable)
    // range: i32 - 2^31-1 = 2147483647

    
    fn main(){
        let x: i32 = 2147483647; //signed integers; otherwise u16: unsigned integers
        let y: u64 = 100;
        println!("Signed number: {}",x);
        println!("Unsigned number: {}",y);

         //=============================================
        //Floats : f32 ,f64

        let pi: f64 = 3.14;
        println!("Value of pi {}",pi);

        //=============================================
        //Boolean values: true/false
        let is_raining = true;
        println!("Is it raining? {}",is_raining);

        //=============================================
        //Character type - char

        let letter =  "h";
        println!("A letter is {}",letter);

    }


   
    
    
