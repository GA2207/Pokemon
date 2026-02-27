import pygame
import sys

# --- 1. CONFIGURATION ET COULEURS ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Couleurs (Charte + Nuances pour le design)
C_VERT_PRAIRIE = "#22C55E"
C_VERT_DECO    = "#16A34A"  # Pour le motif de fond
C_NOIR         = "#1F2937"
C_BLEU_UI      = "#3B82F6"
C_BLEU_SURVOL  = "#60A5FA"  # Plus clair au survol
C_BLEU_OMBRE   = "#1E3A8A"  # Ombre des boutons
C_JAUNE_POK    = "#FDE047"  # Bordure de survol
C_BLANC        = "#FFFFFF"

pygame.init() # Initialisation globale requise pour les polices

# --- 2. CLASSE BOUTON (Version Élaborée) ---
class Bouton:
    def __init__(self, x, y, largeur, hauteur, texte):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.est_survole = False
        self.font = pygame.font.SysFont("impact", 22) # Police plus épaisse

    def dessiner(self, surface):
        # 1. Dessiner l'ombre (décalée vers le bas et la droite)
        ombre_rect = self.rect.copy()
        ombre_rect.x += 4
        ombre_rect.y += 4
        pygame.draw.rect(surface, C_BLEU_OMBRE, ombre_rect, border_radius=12)

        # 2. Apparence du bouton principal selon le survol
        if self.est_survole:
            # Bouton plus clair + Bordure jaune épaisse
            pygame.draw.rect(surface, C_BLEU_SURVOL, self.rect, border_radius=12)
            pygame.draw.rect(surface, C_JAUNE_POK, self.rect, border_radius=12, width=4)
            couleur_texte = C_NOIR
        else:
            # Bouton normal + Bordure discrète
            pygame.draw.rect(surface, C_BLEU_UI, self.rect, border_radius=12)
            pygame.draw.rect(surface, C_BLANC, self.rect, border_radius=12, width=2)
            couleur_texte = C_BLANC

        # 3. Dessiner le texte bien centré
        texte_surface = self.font.render(self.texte, True, couleur_texte)
        texte_rect = texte_surface.get_rect(center=self.rect.center)
        surface.blit(texte_surface, texte_rect)

    def verifier_survol(self, pos_souris):
        self.est_survole = self.rect.collidepoint(pos_souris)

    def est_clique(self, pos_souris):
        return self.rect.collidepoint(pos_souris)


# --- 3. CLASSE PRINCIPALE DU JEU ---
class Jeu:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pokémon - La Plateforme")
        self.clock = pygame.time.Clock()
        
        # Police massive pour le titre
        self.font_titre = pygame.font.SysFont("impact", 75)
        
        self.etat_actuel = "menu"

        # Boutons un peu plus larges et espacés
        centre_x = SCREEN_WIDTH // 2 - 150
        self.boutons_menu = {
            "jouer": Bouton(centre_x, 220, 300, 55, "LANCER UNE PARTIE"),
            "ajouter": Bouton(centre_x, 295, 300, 55, "AJOUTER UN POKÉMON"),
            "pokedex": Bouton(centre_x, 370, 300, 55, "ACCÉDER AU POKÉDEX"),
            "quitter": Bouton(centre_x, 445, 300, 55, "QUITTER")
        }

    def gestion_evenements(self):
        pos_souris = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.etat_actuel == "menu":
                    if self.boutons_menu["jouer"].est_clique(pos_souris):
                        print("BZZZT ! Transition vers le combat !")
                    elif self.boutons_menu["ajouter"].est_clique(pos_souris):
                        print("Ouverture du formulaire...")
                    elif self.boutons_menu["pokedex"].est_clique(pos_souris):
                        print("Ouverture du Pokédex...")
                    elif self.boutons_menu["quitter"].est_clique(pos_souris):
                        pygame.quit()
                        sys.exit()

        if self.etat_actuel == "menu":
            for btn in self.boutons_menu.values():
                btn.verifier_survol(pos_souris)

    def dessiner_fond_menu(self):
        """Dessine un motif de Pokéball géante en filigrane sur le fond"""
        self.screen.fill(C_VERT_PRAIRIE)
        
        centre = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        # Le grand cercle extérieur
        pygame.draw.circle(self.screen, C_VERT_DECO, centre, 300, 25)
        # La ligne horizontale au milieu
        pygame.draw.line(self.screen, C_VERT_DECO, (0, centre[1]), (SCREEN_WIDTH, centre[1]), 25)
        # Le cercle central
        pygame.draw.circle(self.screen, C_VERT_PRAIRIE, centre, 80)
        pygame.draw.circle(self.screen, C_VERT_DECO, centre, 80, 25)

    def afficher_menu(self):
        # 1. Le fond décoré
        self.dessiner_fond_menu()

        # 2. Le titre avec effet d'ombre (Dessiné 2 fois)
        texte_ombre = self.font_titre.render("POKÉMON", True, C_NOIR)
        rect_ombre = texte_ombre.get_rect(center=(SCREEN_WIDTH//2 + 5, 105))
        self.screen.blit(texte_ombre, rect_ombre)

        texte_titre = self.font_titre.render("POKÉMON", True, C_JAUNE_POK)
        rect_titre = texte_titre.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(texte_titre, rect_titre)
        
        # Petit contour noir autour du texte jaune (astuce Pygame)
        contour_titre = self.font_titre.render("POKÉMON", True, C_NOIR)
        self.screen.blit(contour_titre, (rect_titre.x - 2, rect_titre.y))
        self.screen.blit(contour_titre, (rect_titre.x + 2, rect_titre.y))
        self.screen.blit(contour_titre, (rect_titre.x, rect_titre.y - 2))
        self.screen.blit(contour_titre, (rect_titre.x, rect_titre.y + 2))
        self.screen.blit(texte_titre, rect_titre) # On redessine le jaune par dessus

        # 3. Les boutons
        for btn in self.boutons_menu.values():
            btn.dessiner(self.screen)

    def run(self):
        while True:
            self.gestion_evenements()
            if self.etat_actuel == "menu":
                self.afficher_menu()
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Jeu()
    game.run()