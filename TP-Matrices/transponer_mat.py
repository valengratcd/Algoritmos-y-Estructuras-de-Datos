def transponer_mat(mat):
    return list(list(i)for i in zip(*mat))

def main():
    matrix = [
        [1,2,3],
        [4,5,6],
        [3,8,9]
    ]
    print(transponer_mat(matrix))

if __name__ == "__main__":
    main()