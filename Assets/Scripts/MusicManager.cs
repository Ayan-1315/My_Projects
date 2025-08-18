using UnityEngine;

public class MusicManager : MonoBehaviour
{
    public static MusicManager Instance { get; private set; }

    [Header("Assign in Inspector")]
    public AudioSource preTapMusic;   // loop before TapToStart
    public AudioSource gameplayMusic; // loop after TapToStart

    public bool GameStarted { get; private set; } = false;

    private void Awake()
    {
        // Singleton
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject);
            return;
        }
        Instance = this;
        DontDestroyOnLoad(gameObject);

        // Safety: ensure both are not playing on awake
        if (preTapMusic != null) preTapMusic.playOnAwake = false;
        if (gameplayMusic != null) gameplayMusic.playOnAwake = false;
    }

    private void Start()
    {
        // Start with pre-tap music everywhere
        ResetToPreTap();
    }

    // Call when the player FIRST taps to start gameplay
    public void StartGameplay()
    {
        GameStarted = true;
        if (preTapMusic != null && preTapMusic.isPlaying) preTapMusic.Pause();
        if (gameplayMusic != null && !gameplayMusic.isPlaying) gameplayMusic.Play();
    }

    // Call when showing menus or pre-tap state (MainMenu, Settings, Game before start)
    public void ResetToPreTap()
    {
        GameStarted = false;
        if (gameplayMusic != null && gameplayMusic.isPlaying) gameplayMusic.Pause();
        if (preTapMusic != null && !preTapMusic.isPlaying) preTapMusic.Play();
    }

    // Optional for Game Over: pause gameplay loop (you can play a one-shot SFX elsewhere)
    public void PauseGameplay()
    {
        if (gameplayMusic != null && gameplayMusic.isPlaying) gameplayMusic.Pause();
    }
}
