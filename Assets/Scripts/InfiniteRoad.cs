using UnityEngine;

public class InfiniteRoad : MonoBehaviour
{
    public Transform player;
    public GameObject[] roadPrefabs;
    public float roadLength = 50f;
    private float spawnZ = 0f;
    private int roadsOnScreen = 3;
    private float safeZone = 100f;

    private void Start()
    {
        for (int i = 0; i < roadsOnScreen; i++)
        {
            SpawnRoad();
        }
    }

    private void Update()
    {
        if (player.position.z - safeZone > (spawnZ - roadsOnScreen * roadLength))
        {
            SpawnRoad();
        }
    }

    private void SpawnRoad()
    {
        GameObject go = Instantiate(roadPrefabs[Random.Range(0, roadPrefabs.Length)]);
        go.transform.SetParent(transform);
        go.transform.position = Vector3.forward * spawnZ;
        spawnZ += roadLength;
    }
}
