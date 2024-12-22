import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
  } from "@/components/ui/card"

interface Recipe {
    pk_id: number,
    name: string
}

async function getRecipes(): Promise<Recipe[]>{
    const result = await fetch ('http://backend:8000/')

    return result.json()
}

export default async function Page(){
    const recipes = await getRecipes()
    return (
        <main>
            <div className="grid grid-cols-3 gap-8">
                {recipes.map(recipe => (
                    <Card key={recipe.pk_id}>
                        <CardHeader>
                            <div>
                                <CardTitle>{recipe.name}</CardTitle>
                            </div>
                        </CardHeader>
                    </Card>
                ))}
            </div>
        </main>
    )
}