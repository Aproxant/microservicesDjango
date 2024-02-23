import React, { useEffect, useState } from "react";
import Wrapper from "./Wrapper";
import { Link } from "react-router-dom";

const Products =()=>{
    const [products,setProduct]=useState([])
    const getProducts=async ()=>
    {
      const response=await fetch('http://localhost:8000/api/products');
      const data=await response.json()
      console.log(data)
      setProduct(data)
    }

    useEffect(()=>{
      getProducts();
    },[])

    const del= async(id)=>
    {
      if(window.confirm('Are you sure?')){
      const response=await fetch(`http://localhost:8000/api/products/${id}`,
      {
        method: 'DELETE'
      });
      getProducts();
    }
    }

    return (
      <Wrapper>
        <div className="pt-3 pb-2 mb-3 boarder-bottot">
          <div className="btn-toolbar mb-2 mb-md-0">
            <Link to='/admin/products/create' className="btn btn-sm btn-outline-secondary">Add</Link>
          </div>
        </div>
      <div className="table-responsive small">
        <table className="table table-striped table-sm">
          <thead>
            <tr>
              <th scope="col">Id</th>
              <th scope="col">Title</th>
              <th scope="col">Image</th>
              <th scope="col">Likes</th>
            </tr>
          </thead>
          <tbody>
            {
              products.map(p=>{
                return(
                  <tr key={p.id}>
                    <td>{p.id}</td>
                    <td>{p.title}</td>
                    <td><img src={p.image} height="180"/></td>
                    <td>{p.likes}</td>
                    <td>
                      <div className="btn-group mr-2">
                        <Link to={`/admin/products/${p.id}/edit`} className="btn btn-sm btn-outline-secondary">Edit</Link>
                        <a href="#" className="btn btn-sm btn-outline-secondary" onClick={()=>del(p.id)}>Delete</a>
                      </div>
                    </td>
                  </tr>
                )
              })
            }
            
          </tbody>
        </table>
      </div>
      </Wrapper>
    );
}
export default Products