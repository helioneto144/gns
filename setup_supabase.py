#!/usr/bin/env python3
"""
Script para configurar automaticamente o Supabase para o gnS (Genius)
"""

import requests
import json
from config import Config

def test_supabase_connection():
    """Testa a conexão com o Supabase"""
    try:
        url = f"{Config.SUPABASE_URL}/rest/v1/"
        headers = {
            "apikey": Config.SUPABASE_KEY,
            "Authorization": f"Bearer {Config.SUPABASE_KEY}"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status da conexão: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Conexão com Supabase OK!")
            return True
        else:
            print(f"❌ Erro na conexão: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao conectar: {str(e)}")
        return False

def check_members_table():
    """Verifica se a tabela members existe"""
    try:
        url = f"{Config.SUPABASE_URL}/rest/v1/members?select=*&limit=1"
        headers = {
            "apikey": Config.SUPABASE_KEY,
            "Authorization": f"Bearer {Config.SUPABASE_KEY}"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Tabela 'members' existe e está acessível!")
            data = response.json()
            print(f"📊 Registros encontrados: {len(data)}")
            return True
        elif response.status_code == 404:
            print("❌ Tabela 'members' não encontrada!")
            return False
        else:
            print(f"❌ Erro ao acessar tabela: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar tabela: {str(e)}")
        return False

def create_test_member():
    """Cria um membro de teste"""
    try:
        url = f"{Config.SUPABASE_URL}/rest/v1/members"
        headers = {
            "apikey": Config.SUPABASE_KEY,
            "Authorization": f"Bearer {Config.SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        
        test_data = {
            "name": "Teste gnS",
            "commander_name": "TestCommander",
            "phone": "(11) 99999-0000",
            "photo_filename": None
        }
        
        response = requests.post(url, headers=headers, json=test_data, timeout=10)
        
        if response.status_code in [200, 201]:
            print("✅ Membro de teste criado com sucesso!")
            print(f"📝 Dados: {response.json()}")
            return True
        else:
            print(f"❌ Erro ao criar membro: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao criar membro de teste: {str(e)}")
        return False

def main():
    """Função principal"""
    print("🔧 Configurando Supabase para gnS (Genius)...")
    print(f"🌐 URL: {Config.SUPABASE_URL}")
    print(f"🔑 Key: {Config.SUPABASE_KEY[:20]}...")
    print("-" * 50)
    
    # Teste 1: Conexão básica
    print("1️⃣ Testando conexão com Supabase...")
    if not test_supabase_connection():
        print("\n❌ FALHA: Não foi possível conectar ao Supabase!")
        print("\n🔧 Possíveis soluções:")
        print("- Verifique se o projeto Supabase está ativo")
        print("- Confirme a URL e API Key")
        print("- Acesse o dashboard do Supabase para verificar o status")
        return False
    
    # Teste 2: Verificar tabela
    print("\n2️⃣ Verificando tabela 'members'...")
    if not check_members_table():
        print("\n❌ FALHA: Tabela 'members' não encontrada!")
        print("\n🔧 Para criar a tabela:")
        print("1. Acesse https://supabase.com/dashboard")
        print("2. Vá em 'SQL Editor'")
        print("3. Execute o script do arquivo 'supabase_schema.sql'")
        print("4. Execute este script novamente")
        return False
    
    # Teste 3: Criar membro de teste
    print("\n3️⃣ Testando criação de dados...")
    if create_test_member():
        print("\n🎉 SUCESSO: Supabase configurado corretamente!")
        print("\n✅ Próximos passos:")
        print("- A aplicação agora usará Supabase automaticamente")
        print("- Faça deploy da aplicação")
        print("- Acesse o painel admin para gerenciar dados")
        return True
    else:
        print("\n⚠️ AVISO: Conexão OK, mas não foi possível criar dados")
        print("- Verifique as políticas RLS no Supabase")
        print("- Confirme as permissões da API Key")
        return False

if __name__ == "__main__":
    main()
