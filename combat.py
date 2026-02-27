import pygame
import sys
import os

# --- CONFIGURATION ET COULEURS ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

C_FOND_COMBAT  = "#F0FDF4"  # Vert très très clair pour le ciel
C_HERBE        = "#22C55E"  # Vert Prairie (Ta charte)
C_HERBE_SOMBRE = "#16A34A"  # Pour l'ombre sous les Pokémon
C_UI_FOND      = "#FFFFFF"
C_UI_BORDURE   = "#1F2937"
C_PV_MAX       = "#16A34A"  # Barre de vie haute (Vert)
C_NOIR         = "#1F2937"

class EcranCombat:
    def __init__(self, ecran):
        self.screen = ecran
        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        
        # --- CHARGEMENT DES SPRITES ---
        # On utilise os.path.join pour que ça marche sur Windows et Mac
        chemin_joueur = os.path.join("assets", "sprites", "joueur.png")
        chemin_adversaire = os.path.join("assets", "sprites", "adversaire.png")

        # Try/Except au cas où les images sont mal nommées ou manquantes
        try:
            # On charge et on redimensionne un peu les images
            self.sprite_joueur = pygame.image.load(chemin_joueur).convert_alpha()
            self.sprite_joueur = pygame.transform.scale(self.sprite_joueur, (200, 200))
            
            self.sprite_adversaire = pygame.image.load(chemin_adversaire).convert_alpha()
            self.sprite_adversaire = pygame.transform.scale(self.sprite_adversaire, (180, 180))
            print("Sprites chargés avec succès !")
        except FileNotFoundError:
            print("⚠️ ATTENTION : Images non trouvées dans assets/sprites/.")
            print("Assure-toi de les nommer 'joueur.png' et 'adversaire.png'")
            # On crée des carrés de remplacement si l'image manque
            self.sprite_joueur = pygame.Surface((200, 200))
            self.sprite_joueur.fill((0, 0, 255)) 
            self.sprite_adversaire = pygame.Surface((180, 180))
            self.sprite_adversaire.fill((255, 0, 0))

    def dessiner_arene(self):
        # Fond (Ciel)
        self.screen.fill(C_FOND_COMBAT)
        
        # Socle Adversaire (En haut à droite)
        pygame.draw.ellipse(self.screen, C_HERBE, (450, 150, 250, 80))
        pygame.draw.ellipse(self.screen, C_HERBE_SOMBRE, (450, 150, 250, 80), 4)

        # Socle Joueur (En bas à gauche)
        pygame.draw.ellipse(self.screen, C_HERBE, (100, 380, 300, 100))
        pygame.draw.ellipse(self.screen, C_HERBE_SOMBRE, (100, 380, 300, 100), 5)

    def dessiner_ui_stats(self, x, y, nom, niveau, pv_actuel, pv_max):
        """Dessine les cadres avec les noms et les barres de vie"""
        # Fond de la carte de stats
        rect_ui = pygame.Rect(x, y, 250, 80)
        pygame.draw.rect(self.screen, C_UI_FOND, rect_ui, border_radius=10)
        pygame.draw.rect(self.screen, C_UI_BORDURE, rect_ui, border_radius=10, width=3)

        # Textes
        texte_nom = self.font.render(f"{nom}  Niv.{niveau}", True, C_NOIR)
        self.screen.blit(texte_nom, (x + 15, y + 10))

        # Barre de vie (Fond gris, puis jauge verte)
        pygame.draw.rect(self.screen, "#D1D5DB", (x + 15, y + 45, 200, 15), border_radius=5)
        
        # Calcul de la largeur de la barre verte en fonction des PV
        pourcentage_pv = pv_actuel / pv_max
        largeur_barre_verte = int(200 * pourcentage_pv)
        pygame.draw.rect(self.screen, C_PV_MAX, (x + 15, y + 45, largeur_barre_verte, 15), border_radius=5)

    def dessiner(self):
        self.dessiner_arene()

        # Affichage des Sprites sur leurs socles
        # On ajuste les coordonnées pour qu'ils soient bien posés
        self.screen.blit(self.sprite_adversaire, (485, 40)) 
        self.screen.blit(self.sprite_joueur, (150, 220))

        # Affichage des interfaces de vie
        # Stats Adversaire (En haut à gauche)
        self.dessiner_ui_stats(50, 50, "Florizarre", 50, 100, 100)
        # Stats Joueur (En bas à droite)
        self.dessiner_ui_stats(500, 350, "Dracaufeu", 50, 100, 100)

# --- ZONE DE TEST POUR VOIR L'ÉCRAN ---
if __name__ == "__main__":
    pygame.init()
    ecran = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Test Arène")
    horloge = pygame.time.Clock()
    
    combat = EcranCombat(ecran)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        combat.dessiner()
        pygame.display.flip()
        horloge.tick(FPS)