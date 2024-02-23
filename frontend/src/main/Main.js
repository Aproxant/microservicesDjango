import React, { useEffect, useState } from "react";

const Main=()=>
{
    const [products,setProducts]=useState([]);

    const getData= async ()=>{
      const response = await fetch('http://localhost:8000/api/products');
      const data=await response.json()
      setProducts(data);

    }
    
    useEffect(()=>
    {
      getData();
    },[]);

    const like= async (num)=>{
      await fetch(`http://localhost:8001/api/products/${num}/like`,{
        method: 'POST',
        headers: {'Content-Type': 'application-json'}
      });
      setProducts(products.map(p=>{
        if (p.id===num)
        {
          p.likes++;
        }
        return p;
      }))
    }
    return (
<main>


<div class="album py-5 bg-body-tertiary">
  <div class="container">
    <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-3">
      {products.map(p=>{
        return(
        <div class="col">
        <div class="card shadow-sm">
          <img src={p.image}/>
          <div class="card-body">
            <p class="card-text">{p.title}</p>
            <div class="d-flex justify-content-between align-items-center">
              <div class="btn-group">
                <button type="button" class="btn btn-sm btn-outline-secondary" onClick={()=>like(p.id)}>Like</button>
                
              </div>
              <small class="text-body-secondary">{p.likes}</small>
            </div>
          </div>
        </div>
      </div>  
        );
      })}
          
    </div>
  </div>
</div>

</main>

    );
}
export default Main;