from src.game import Game


def main():
    game = Game()
    try:
        game.run()
    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        game.cleanup()


if __name__ == "__main__":
    main()
