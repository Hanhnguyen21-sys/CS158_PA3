
//entry points should be main()

fn main(){
    tell_height(157);
    human_id("Nguyen",23,156.5);
    //function calculate total price
    let _x: i32 ={
        let price: i32=8;
        let qty: i32 = 4;
        price*qty
    };
    println!("Result: {}",_x);
    let r: i32 = add(5,6);
    println!("{}",r);
    println!("My BMI: {:.2}",bmi(1.57,46.0));

}

//hoisting - can call function anywhere

//function with parameters
fn tell_height(height: i32){
    println!("The height is: {} cm",height);

}


// multiple parameters
fn human_id(name: &str,age: u32, height: f32)
{
    println!("Name: {}, I am {} years old, and my height is {} cm",name,age,height);
}


//expressions (returns a value) Ex: add(3,4), true, 5, etc

fn add(a: i32, b: i32) -> i32 {a+b}

//statements (not returns a value
// Ex: let x =10;
// fn foo(){}
// control flow statements: if condition{//code}


fn bmi(height: f32, kg: f32 )->f32 {
    (kg)/(height*height)
}



