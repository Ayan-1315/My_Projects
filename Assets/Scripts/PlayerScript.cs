using UnityEngine;

public class PlayerScript : MonoBehaviour
{
    public Rigidbody rb;
    public float speed = 10f;       // Left/Right movement speed
    public float force = 1000f;     // Forward force
    public float minX;              // Left boundary
    public float maxX;              // Right boundary
    public float jumpForce = 5f;    // Jump strength

    private bool isGrounded = true; // Ground check

    // Swipe detection
    private Vector2 startTouchPos;
    private Vector2 endTouchPos;
    private float swipeThreshold = 50f; // Minimum swipe distance

    void Start()
    {
        if (rb == null)
            rb = GetComponent<Rigidbody>();
    }

    void Update()
    {
        // Clamp player movement within minX and maxX
        Vector3 playerPos = transform.position;
        playerPos.x = Mathf.Clamp(playerPos.x, minX, maxX);
        transform.position = playerPos;

        HandleTouchInput();
    }

    private void FixedUpdate()
    {
        // Always move forward
        rb.AddForce(0, 0, force * Time.deltaTime);
    }

    private void OnCollisionEnter(Collision collision)
    {
        // Reset jump ability when touching ground
        if (collision.gameObject.CompareTag("Ground"))
        {
            isGrounded = true;
        }
    }

    void HandleTouchInput()
    {
        if (Input.touchCount > 0)
        {
            Touch touch = Input.GetTouch(0);

            // Detect swipe
            if (touch.phase == TouchPhase.Began)
            {
                startTouchPos = touch.position;
            }
            else if (touch.phase == TouchPhase.Ended)
            {
                endTouchPos = touch.position;
                Vector2 swipeDelta = endTouchPos - startTouchPos;

                if (swipeDelta.magnitude > swipeThreshold && Mathf.Abs(swipeDelta.y) > Mathf.Abs(swipeDelta.x))
                {
                    if (swipeDelta.y > 0)
                        Jump();
                }
            }

            // Continuous hold for movement
            if (touch.phase == TouchPhase.Stationary || touch.phase == TouchPhase.Moved)
            {
                if (touch.position.x < Screen.width / 2)
                {
                    // Left side
                    MoveLeft();
                }
                else
                {
                    // Right side
                    MoveRight();
                }
            }
        }
    }

    void MoveLeft()
    {
        transform.position += new Vector3(-speed * Time.deltaTime, 0, 0);
    }

    void MoveRight()
    {
        transform.position += new Vector3(speed * Time.deltaTime, 0, 0);
    }

    void Jump()
    {
        if (isGrounded)
        {
            rb.AddForce(Vector3.up * jumpForce, ForceMode.Impulse);
            isGrounded = false;
        }
    }
}
