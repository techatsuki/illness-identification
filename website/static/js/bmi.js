const heightInput = document.querySelector(".heightInput");
const weightInput = document.querySelector(".weightInput");
const button = document.querySelector("button");
const result = document.querySelector(".result");
const condition = document.querySelector("span");

/*  formula BMI  */ 
/* 70/(170/100)^2 */

function compute(){
    condition.innerText = "";
    let a = +heightInput.value/100;
    let b = Math.pow(a,2);
    let c = +weightInput.value/b;
    result.innerText = c.toFixed(2);
    if(heightInput.value >0 && weightInput.value >0){
        if(result.innerText < 18.5){
            condition.innerText = "Underweight";
        }else if(result.innerText >=18.5 && result.innerText <= 25){
            condition.innerText = "Normal";
        }else if(result.innerText >25 && result.innerText <= 35){
            condition.innerText = "Overweight";
        }else{
            condition.innerText = "Obesity";
        }
    }else{
        result.innerText = "ENTER VALID VALUES";
    }
}

button.addEventListener("click", compute);