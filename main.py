import os
import sys
from tabulate import tabulate
from models import Song
from repository import MusicRepository
from player import MusicPlayer, PlayerObserver

class CLIObserver(PlayerObserver):
    def on_song_start(self, song):
        print(f"\n>>> Reproduzindo agora: {song}")

    def on_song_end(self):
        print("\n>>> Fim da reprodução.")

class SoundWaveCLI:
    def __init__(self):
        self.repo = MusicRepository()
        self.player = MusicPlayer()
        self.player.add_observer(CLIObserver())
        self.running = True

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_menu(self):
        menu = [
            ["1", "Adicionar Música à Biblioteca"],
            ["2", "Listar Biblioteca / Tocar"],
            ["3", "Play/Pause"],
            ["4", "Parar"],
            ["5", "Próxima"],
            ["6", "Gerenciar Playlists"],
            ["7", "Histórico"],
            ["0", "Sair"]
        ]
        print("\n=== SOUNDWAVE MUSIC PLAYER ===")
        if self.player.current_song:
            status = "PAUSADO" if self.player.is_paused else "TOCANDO"
            print(f"Status: [{status}] {self.player.current_song}")
        print(tabulate(menu, headers=["Opção", "Ação"]))

    def run(self):
        while self.running:
            self.show_menu()
            choice = input("\nEscolha uma opção: ")

            if choice == "1":
                raw_path = input("Caminho do arquivo (mp3/wav): ").strip()
                path = raw_path.strip('"').strip("'")
                path = os.path.normpath(path)
                
                if os.path.exists(path) and os.path.isfile(path):
                    song = Song(path)
                    if self.repo.add_song(song):
                        print(f"Música '{song.title}' adicionada com sucesso!")
                    else:
                        print("Música já existe na biblioteca.")
                else:
                    print(f"Erro: Arquivo não encontrado em: {path}")
                    print("Dica: Certifique-se de que o caminho está correto e o arquivo existe.")

            elif choice == "2":
                if not self.repo.songs:
                    print("Biblioteca vazia.")
                else:
                    table = [[i, s.artist, s.title] for i, s in enumerate(self.repo.songs)]
                    print(tabulate(table, headers=["ID", "Artista", "Título"]))
                    idx = input("\nDigite o ID para tocar (ou Enter para voltar): ")
                    if idx.isdigit() and int(idx) < len(self.repo.songs):
                        self.player.play_song(self.repo.songs[int(idx)])

            elif choice == "3":
                self.player.pause_resume()

            elif choice == "4":
                self.player.stop_playback()

            elif choice == "5":
                self.player.next_song()

            elif choice == "6":
                self.manage_playlists()

            elif choice == "7":
                if self.player.history.is_empty():
                    print("Histórico vazio.")
                else:
                    print("\n--- Histórico (Recentes primeiro) ---")
                    temp_stack = []
                    while not self.player.history.is_empty():
                        s = self.player.history.pop()
                        print(f"- {s}")
                        temp_stack.append(s)
                    for s in reversed(temp_stack):
                        self.player.history.push(s)

            elif choice == "0":
                self.player.stop_playback()
                self.running = False
                print("Até logo!")

    def manage_playlists(self):
        print("\n--- Playlists ---")
        names = list(self.repo.playlists.keys())
        if not names:
            print("Nenhuma playlist criada.")
        else:
            for i, name in enumerate(names):
                print(f"{i}: {name}")
        
        print("\na: Criar | v: Ver/Editar | d: Excluir Playlist | s: Sair")
        cmd = input("Escolha: ")
        
        if cmd == 'a':
            name = input("Nome da nova playlist: ")
            self.repo.create_playlist(name)
            print(f"Playlist '{name}' criada!")
            
        elif cmd == 'd' and names:
            idx = input("ID da playlist para excluir: ")
            if idx.isdigit() and int(idx) < len(names):
                name = names[int(idx)]
                self.repo.delete_playlist(name)
                print(f"Playlist '{name}' excluída!")

        elif cmd == 'v' and names:
            idx = input("ID da playlist: ")
            if not idx.isdigit() or int(idx) >= len(names): return
            
            name = names[int(idx)]
            while True:
                songs_paths = self.repo.playlists[name]
                print(f"\n=== Playlist: {name} ===")
                if not songs_paths:
                    print("(Vazia)")
                else:
                    for i, p in enumerate(songs_paths):
                        song = next((s for s in self.repo.songs if s.file_path == p), None)
                        print(f"{i}: {song if song else p}")
                
                print("\nt: Tocar Playlist | +: Add Música | -: Remover Música | s: Voltar")
                sub_cmd = input("Escolha: ")
                
                if sub_cmd == 't' and songs_paths:
                    self.player.queue.clear()
                    for p in songs_paths:
                        song = next((s for s in self.repo.songs if s.file_path == p), None)
                        if song: self.player.queue.enqueue(song)
                    self.player.next_song()
                    break
                elif sub_cmd == '+':
                    if not self.repo.songs:
                        print("Biblioteca vazia! Adicione músicas primeiro.")
                    else:
                        table = [[i, s.artist, s.title] for i, s in enumerate(self.repo.songs)]
                        print(tabulate(table, headers=["ID", "Artista", "Título"]))
                        m_idx = input("ID da música para adicionar: ")
                        if m_idx.isdigit() and int(m_idx) < len(self.repo.songs):
                            self.repo.add_to_playlist(name, self.repo.songs[int(m_idx)].file_path)
                            print("Música adicionada!")
                elif sub_cmd == '-':
                    if not songs_paths:
                        print("Playlist já está vazia.")
                    else:
                        m_idx = input("ID da música para remover: ")
                        if m_idx.isdigit() and int(m_idx) < len(songs_paths):
                            path_to_remove = songs_paths[int(m_idx)]
                            self.repo.remove_from_playlist(name, path_to_remove)
                            print("Música removida!")
                elif sub_cmd == 's':
                    break

if __name__ == "__main__":
    app = SoundWaveCLI()
    app.run()
