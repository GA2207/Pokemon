import pygame
import sys

# --- 1. CONFIGURATION ET COULEURS (Ta Charte) ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Couleurs Officielles (Document fourni)
C_VERT_PRAIRIE = "#22C55E"  # Fond du jeu
C_NOIR         = "#1F2937"  # Texte
C_BLEU_UI      = "#3B82F6"  # Boutons
C_BLANC        = "#FFFFFF"

class Jeu:
    def __init__(self):
        # Initialisation de Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pokémon - La Plateforme")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 30)
        
        # État du jeu : 'menu', 'combat', 'pokedex'
        self.etat_actuel = "menu"

    def gestion_evenements(self):
        """Gère les clics et le clavier"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Exemple de clic souris (à développer)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.etat_actuel == "menu":
                    print("Clic dans le menu (coordonnées):", event.pos)
                    # Ici on mettra la logique pour changer d'écran

    def afficher_menu(self):
        """Dessine l'écran du Menu"""
        self.screen.fill(C_VERT_PRAIRIE) # Fond Vert Prairie

        # Titre temporaire
        texte_titre = self.font.render("POKÉMON", True, C_NOIR)
        rect_titre = texte_titre.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(texte_titre, rect_titre)

        # Simulation de boutons (On fera une vraie classe Bouton après)
        pygame.draw.rect(self.screen, C_BLEU_UI, (300, 200, 200, 50)) # Bouton Jouer
        texte_bouton = self.font.render("JOUER", True, C_BLANC)
        self.screen.blit(texte_bouton, (360, 210))

    def run(self):
        """Boucle principale du jeu"""
        while True:
            self.gestion_evenements()

            # Gestion de l'affichage selon l'état
            if self.etat_actuel == "menu":
                self.afficher_menu()
            elif self.etat_actuel == "combat":
                pass # On codera ça plus tard
            
            # Mise à jour de l'écran
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Jeu()
    game.run()