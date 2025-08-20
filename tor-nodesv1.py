import requests
from bs4 import BeautifulSoup
import csv
import sys

def scrape_tor_nodes():
    """
    Récupère les adresses IP et ports depuis la page des nœuds Tor
    """
    url = "https://www.dan.me.uk/tornodes"
    
    try:
        print("Récupération de la page...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        print("Analyse du contenu HTML...")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        table = soup.find('table')
        if not table:
            print("Erreur : Impossible de trouver la table dans la page")
            return []
        
        nodes = []
        rows = table.find_all('tr')
        
        for row in rows[1:]:
            cells = row.find_all('td')
            if len(cells) >= 3:  
                ip_address = cells[0].get_text(strip=True)
                port = cells[2].get_text(strip=True) 
                
                if port and port != '-':
                    nodes.append(f"{ip_address},{port}")
        
        return nodes
    
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération de la page : {e}")
        return []
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return []

def save_to_file(nodes, filename="tor_nodes.txt"):
    try:
        with open(filename, 'w', newline='') as f:
            f.write("ip_address,port\n")
            for node in nodes:
                f.write(node + '\n')
        print(f"✓ {len(nodes)} nœuds sauvegardés dans '{filename}'")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")

def main():
  
    print("=== Scraper de nœuds Tor ===\n")
    
    # Scraper les données
    nodes = scrape_tor_nodes()
    
    if nodes:
        print(f"\n✓ {len(nodes)} nœuds trouvés")
        
        print("\nExemple des 10 premiers nœuds :")
        print("-" * 30)
        for node in nodes[:10]:
            print(node)
        
        print("\nSauvegarde des données...")
        save_to_file(nodes)
        
        if len(nodes) > 10:
            response = input(f"\nVoulez-vous afficher tous les {len(nodes)} nœuds ? (o/n) : ")
            if response.lower() == 'o':
                print("\nTous les nœuds :")
                print("-" * 30)
                for node in nodes:
                    print(node)
    else:
        print("Aucun nœud trouvé ou erreur lors du scraping")

if __name__ == "__main__":
    main()