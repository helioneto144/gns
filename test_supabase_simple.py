#!/usr/bin/env python3
"""
Teste simples do Supabase
"""

from config import Config

def main():
    print("🔧 Status da Configuração Supabase:")
    print(f"URL: {Config.SUPABASE_URL}")
    print(f"Key: {Config.SUPABASE_KEY[:20]}...")
    
    # Teste de importação
    try:
        from supabase import create_client
        print("✅ Biblioteca Supabase: OK")
    except ImportError as e:
        print(f"❌ Biblioteca Supabase: {e}")
        return
    
    # Teste de conexão
    try:
        supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
        print("✅ Cliente Supabase: Criado")
        
        # Teste simples
        result = supabase.table("members").select("*").limit(1).execute()
        print(f"✅ Teste de consulta: {len(result.data)} registros")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        print("\n🔧 Possíveis problemas:")
        print("1. Projeto Supabase inativo")
        print("2. Tabela 'members' não existe")
        print("3. API Key inválida")
        print("\n📋 Para corrigir:")
        print("1. Acesse https://supabase.com/dashboard")
        print("2. Ative o projeto")
        print("3. Execute o SQL do arquivo supabase_schema.sql")

if __name__ == "__main__":
    main()
