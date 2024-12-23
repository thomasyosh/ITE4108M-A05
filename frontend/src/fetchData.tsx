"use server"

export async function fetchData(){
    const result = await fetch ('http://backend:8000/')

    return result.json()
}