using UnityEngine;

public class CollectibleSpawner : MonoBehaviour
{
    public GameObject collectiblePrefab;
    public Transform player;
    public float spawnDistance = 50f;
    public float minSpacing = 10f;
    public float maxSpacing = 20f;

    [Header("Overlap Settings")]
    public float checkRadius = 1f; // how far to check around spawn point

    private float nextSpawnZ = 0f;

    private void Update()
    {
        if (player.position.z + spawnDistance > nextSpawnZ)
        {
            Vector3 spawnPos = FindSafeSpawnPoint(nextSpawnZ);

            if (spawnPos != Vector3.zero)
            {
                Instantiate(collectiblePrefab, spawnPos, Quaternion.identity);
            }

            nextSpawnZ += Random.Range(minSpacing, maxSpacing);
        }
    }

    private Vector3 FindSafeSpawnPoint(float zPos)
    {
        int attempts = 5; // try a few times then skip
        while (attempts-- > 0)
        {
            float spawnX = Random.Range(-15.2f, -6.5f);
            Vector3 candidate = new Vector3(spawnX, 1f, zPos);

            // Check for obstacles nearby using tag
            Collider[] hits = Physics.OverlapSphere(candidate, checkRadius);
            bool blocked = false;

            foreach (Collider hit in hits)
            {
                if (hit.CompareTag("obstacles"))
                {
                    blocked = true;
                    break;
                }
            }

            if (!blocked)
            {
                return candidate;
            }
        }

        return Vector3.zero; // skip if no safe spot found
    }
}

