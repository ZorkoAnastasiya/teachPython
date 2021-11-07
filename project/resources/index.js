const TASK_1_URL = '/sum_cube/';
const TASK_3_URL = '/prime_numbers/';


async function api_call_get(url){
    const request = await fetch(
        url, {
            method: "GET"
    });
    const payload = await request.json()
    return payload
}

async function cube(number){
    const url = TASK_1_URL + number;
    const payload = await api_call_get(url);
    return payload.data;
}

async function prime_numbers(number){
    const url = TASK_3_URL + number;
    const payload = await api_call_get(url);
    return payload.data;
}

async function setUpTask1(){
    let input = document.querySelector("#task_1 input");
    let span = document.querySelector("#task_1 span");

    input.addEventListener("input", async function(){
        const number = input.value;
        const result = await cube(number);
        span.textContent = result;
    });
}

async function setUpTask3(){
    let input = document.querySelector("#task_3 input");
    let span = document.querySelector("#task_3 span");

    input.addEventListener("input", async function(){
        const number = input.value;
        const result = await prime_numbers(number);
        span.textContent = result;
    });
}

async function setUP(){
    await setUpTask1();
    await setUpTask3();
}

document.addEventListener("DOMContentLoaded", setUP);