from fastapi import APIRouter, HTTPException
from controllers.sites_controller import SitesController
from models.sites_model import Sites

router = APIRouter()
new_sites = SitesController()


@router.get("/get/sites")
async def get_sites():
    rpta = new_sites.get_sites()
    return rpta


@router.get("/get/sites/{idSite}")
async def get_sites_id(idSite: int):
    rpta = new_sites.get_sites_id(idSite)
    return rpta


@router.post("/post/sites")
async def post_sites(newsites: Sites):
    rpta = new_sites.post_sites(newsites)
    return rpta


@router.put("/update/sites/{idSite}")
async def update_sites(idSite: int, newsites: Sites):
    rpta = new_sites.update_sites(idSite, newsites)
    return rpta


@router.delete("/delete/sites/{idSite}")
async def delete_sites(idSite: int):
    rpta = new_sites.delete_sites(idSite)
    return rpta
