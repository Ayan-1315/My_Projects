using UnityEngine;

public class PlayerCollision : MonoBehaviour
{
    public PlayerScript playerScript;
    public GameController gameController;
    public Score scoreManager;

    public AudioSource collectMusic;      // On collect
    public AudioSource gameOverMusic;     // On game over

    private bool isGameOver = false;

    private void Update()
    {
        // Check if player falls off the road
        if (!isGameOver && transform.position.y < -5f)
        {
            HandleGameOver();
        }
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Collectables"))
        {
            if (collectMusic != null)
                collectMusic.Play();

            scoreManager.AddCollectible();
            other.gameObject.SetActive(false);
        }
    }

    private void OnCollisionEnter(Collision other)
    {
        if (other.gameObject.CompareTag("obstacles") && !isGameOver)
        {
            HandleGameOver();
        }
    }

    private void HandleGameOver()
    {
        isGameOver = true;

        if (gameOverMusic != null)
            gameOverMusic.Play();

        scoreManager.ShowFinalScore();
        gameController.GameOver();
        playerScript.enabled = false;
    }
}
