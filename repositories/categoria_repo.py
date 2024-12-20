import json
import sqlite3
from typing import List, Optional
from models.categoria_model import Categoria
from sql.categoria_sql import SQL_ALTERAR, SQL_CRIAR_TABELA, SQL_EXCLUIR, SQL_INSERIR, SQL_OBTER_QUANTIDADE, SQL_OBTER_TODOS, SQL_OBTER_UM
from util.database import obter_conexao 

class CategoriaRepo:

    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA)
            
    @classmethod
    def inserir(cls, categoria: Categoria) -> Optional[Categoria]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_INSERIR, (categoria.nome,))
                if cursor.rowcount > 0:
                    categoria.id = cursor.lastrowid
                    return categoria
        except sqlite3.Error as ex:
            print(ex)
            return None
    
    @classmethod
    def obter_todos(cls) -> List[Categoria]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(SQL_OBTER_TODOS).fetchall()
                categorias = [Categoria(*t) for t in tuplas]
                return categorias
        except sqlite3.Error as ex:
            print(ex)
            return None
    
    @classmethod
    def alterar(cls, categoria: Categoria) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_ALTERAR, (categoria.nome, categoria.id))
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False
    
    @classmethod
    def excluir(cls, id: int) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_EXCLUIR, (id,))
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False
    
    @classmethod
    def obter_um(cls, id: int) -> Optional[Categoria]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_UM, (id,)).fetchone()
                if not tupla: return None
                categoria = Categoria(*tupla)
                return categoria
        except sqlite3.Error as ex:
            print(ex)
            return None
        
    @classmethod
    def obter_quantidade(cls) -> Optional[int]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_QUANTIDADE).fetchone()
                return int(tupla[0])
        except sqlite3.Error as ex:
            print(ex)
            return None
    
    @classmethod
    def inserir_categorias_json(cls, arquivo_json: str):
        if CategoriaRepo.obter_quantidade() == 0:
            with open(arquivo_json, "r", encoding="utf-8") as arquivo:
                categorias = json.load(arquivo)
                for categoria in categorias:
                    CategoriaRepo.inserir(Categoria(**categoria))
        
    