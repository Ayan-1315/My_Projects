using UnityEngine;
using UnityEngine.SceneManagement;

public class GameController : MonoBehaviour
{
    public GameObject gameOverPanel;
    public GameObject TapToStart;
    public GameObject ScoreText;

    private bool isGameOver = false;
    private bool gameStarted = false;

    private CanvasGroup tapCanvasGroup;
    private CanvasGroup scoreCanvasGroup;
    private float blinkSpeed = 2.5f; // Blink speed

    private void Start()
    {
        // Get CanvasGroup components for fade effects
        tapCanvasGroup = TapToStart.GetComponent<CanvasGroup>();
        scoreCanvasGroup = ScoreText.GetComponent<CanvasGroup>();

        if (tapCanvasGroup == null) tapCanvasGroup = TapToStart.AddComponent<CanvasGroup>();
        if (scoreCanvasGroup == null) scoreCanvasGroup = ScoreText.AddComponent<CanvasGroup>();

        TapToStart.SetActive(true);
        ScoreText.SetActive(true); // We use alpha to hide instead of disabling
        scoreCanvasGroup.alpha = 0; // Hide score at start

        if (gameOverPanel != null)
            gameOverPanel.SetActive(false);
        else
            Debug.LogWarning("Game Over Panel is not assigned in GameController!");

        PauseGame(0);
    }

    private void Update()
    {
        // Blink "Tap To Start" until game starts
        if (!gameStarted)
        {
            float alpha = (Mathf.Sin(Time.unscaledTime * blinkSpeed) + 1) / 2;
            tapCanvasGroup.alpha = alpha;

            if (Input.GetKeyDown(KeyCode.Mouse0))
            {
                StartGame();
            }
        }
    }

    public void GameOver()
    {
        MusicManager.Instance?.PauseGameplay(); // gameplay loop off; you can play a GameOver SFX separately
        if (!isGameOver)
        {
            isGameOver = true;
            if (gameOverPanel != null)
            {
                gameOverPanel.SetActive(true);
                scoreCanvasGroup.alpha = 0; // Hide score on game over
            }
            PauseGame(0);
        }
    }

    public void Restart()
    {
        MusicManager.Instance?.ResetToPreTap();
        PauseGame(1);
        SceneManager.LoadScene(SceneManager.GetActiveScene().name);
    }

    public void QuitGame()
    {
        Application.Quit();
    }

    public void PauseGame(int x)
    {
        Time.timeScale = x;
    }

    public void StartGame()
    {
        MusicManager.Instance?.StartGameplay();
        gameStarted = true;
        TapToStart.SetActive(false);
        StartCoroutine(FadeInScore());
        PauseGame(1);
    }

    private System.Collections.IEnumerator FadeInScore()
    {
        float duration = 0.5f;
        float time = 0;
        while (time < duration)
        {
            scoreCanvasGroup.alpha = Mathf.Lerp(0, 1, time / duration);
            time += Time.unscaledDeltaTime;
            yield return null;
        }
        scoreCanvasGroup.alpha = 1;
    }
}
