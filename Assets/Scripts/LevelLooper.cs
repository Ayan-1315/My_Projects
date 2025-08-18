using UnityEngine;

public class LevelLooper : MonoBehaviour
{
    [Header("Setup")]
    public Transform player;            // your player
    public Transform[] segments;        // assign 2–3 copies of your level chunk, placed in order on Z
    public float segmentLength = 100f;  // exact Z-length of ONE chunk (distance from start to end)

    [Header("Reset on recycle")]
    public bool reactivateCollectables = true;
    public bool reactivateObstacles = false; // set true if you disable/destroy obstacles

    void Update()
    {
        if (segments == null || segments.Length == 0 || player == null) return;

        // find back-most and front-most segments by Z
        Transform back = segments[0];
        Transform front = segments[0];

        for (int i = 1; i < segments.Length; i++)
        {
            if (segments[i].position.z < back.position.z) back = segments[i];
            if (segments[i].position.z > front.position.z) front = segments[i];
        }

        // if player has fully passed the back segment, recycle it to the front
        if (player.position.z - back.position.z >= segmentLength)
        {
            Vector3 p = back.position;
            p.z = front.position.z + segmentLength;
            back.position = p;

            // Reset contents so it feels new again
            ResetSegment(back.gameObject);
        }
    }

    void ResetSegment(GameObject segmentRoot)
    {
        if (reactivateCollectables)
        {
            var collectables = segmentRoot.GetComponentsInChildren<Transform>(true);
            foreach (var t in collectables)
            {
                if (t.CompareTag("Collectables")) t.gameObject.SetActive(true);
            }
        }

        if (reactivateObstacles)
        {
            var obstacles = segmentRoot.GetComponentsInChildren<Transform>(true);
            foreach (var t in obstacles)
            {
                if (t.CompareTag("obstacles")) t.gameObject.SetActive(true);
            }
        }
    }
}
