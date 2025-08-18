using UnityEngine;
using UnityEngine.UI; // Legacy UI Text

public class Score : MonoBehaviour
{
    public Transform player;
    public Text scoreText;         // In-game score (distance only)
    public Text FinalScoreText;    // Game Over panel total score
    public Text CubeCollectText;   // Shows cubes collected during run
    public Text GameOverScoreText; // Game Over panel "Score:" text (distance only)
    public Text HighScoreText;     // Game Over panel high score

    private float startZ;
    private int distanceScore = 0;
    private int cubeCount = 0;
    private int highScore = 0;

    void Start()
    {
        startZ = player.position.z;

        // Load saved high score
        highScore = PlayerPrefs.GetInt("HighScore", 0);

        if (HighScoreText != null)
            HighScoreText.text = "High Score : " + highScore;
    }

    void Update()
    {
        // Distance score only
        distanceScore = Mathf.FloorToInt(player.position.z - startZ);
        scoreText.text = "" + distanceScore;

        // Update in-game cube counter
        CubeCollectText.text = "Cubes : " + cubeCount;
    }

    public void AddCollectible()
    {
        cubeCount++;
    }

    public void ShowFinalScore()
    {
        // Show raw distance score on Game Over panel
        GameOverScoreText.text = "Distance : " + distanceScore;

        // Show total score (distance + cube bonus)
        int totalScore = distanceScore + (cubeCount * 10);
        FinalScoreText.text = "Total Score : " + totalScore;

        // Check and update High Score
        if (totalScore > highScore)
        {
            highScore = totalScore;
            PlayerPrefs.SetInt("HighScore", highScore);
            PlayerPrefs.Save();
        }

        if (HighScoreText != null)
            HighScoreText.text = "High Score : " + highScore;
    }

    public void ResetScore()
    {
        distanceScore = 0;
        cubeCount = 0;
        scoreText.text = "0";
        CubeCollectText.text = "Cubes : 0";
    }
}
