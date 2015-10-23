#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include <openssl/ec.h>

#include "block.h"
#include "common.h"
#include "transaction.h"

/* Usage: ./balances *.blk
 * Reads in a list of block files and outputs a table of public key hashes and
 * their balance in the longest chain of blocks. In case there is more than one
 * chain of the longest length, chooses one arbitrarily. */

/* If a block has height 0, it must have this specific hash. */
const hash_output GENESIS_BLOCK_HASH = {
	0x00, 0x00, 0x00, 0x0e, 0x5a, 0xc9, 0x8c, 0x78, 0x98, 0x00, 0x70, 0x2a, 0xd2, 0xa6, 0xf3, 0xca,
	0x51, 0x0d, 0x40, 0x9d, 0x6c, 0xca, 0x89, 0x2e, 0xd1, 0xc7, 0x51, 0x98, 0xe0, 0x4b, 0xde, 0xec,
};

struct blockchain_node {
	struct blockchain_node *parent;
	struct block b;
	int is_valid;
	int order;
};

/* A simple linked list to keep track of account balances. */
struct balance {
	struct ecdsa_pubkey pubkey;
	int balance;
	struct balance *next;
};

/* function that checks for validness of a block
	return 0 if not valid
	return 1 if valid
*/
int validness_test (const struct blockchain_node *node, int argc) {

	hash_output hop;

    // for (int i =1; i < argc; i++) {
	// printf("block b's height: [%u] \n",array_of_block[i].b.height);

	// FIRST BULLET POINT

	// check the block that has height 0 must have genesis value
	if (node->b.height == 0) {

		block_hash(&node->b, hop);
		if (byte32_cmp(GENESIS_BLOCK_HASH, hop) != 0) {
			printf("INI GOBLOK TES 1!!! \n\n");
			return 0;
		}
	}

	// if the block has height >= 1, its parent must be a valid parent with height h-1
	else if (node->b.height >= 1) {

		if (node->parent->is_valid != 1) {
			printf("INI GOBLOK TES 1.2!!! \n\n");
			return 0;
		}

		if (node->parent->b.height != node->b.height - 1) {
			printf("INI GOBLOK TES 1.3!!! \n\n");
			return 0;
		}
	}

	// SECOND BULLET POINT

	// The hash of the block must be smaller than TARGET_HASH; i.e., it must start with 24 zero bits.
	hash_output test_target_hash;
	block_hash(&node->b, test_target_hash);
	if (hash_output_is_below_target(test_target_hash) == 0) {
		printf("INI GOBLOK TES 2!!! \n\n");
		return 0;
	}

	// THIRD BULLET POINT

	// The height of both of the block's transactions must be equal to the block's height.
	int height_of_block = node->b.height;
	int height_trans_1 = node->b.reward_tx.height;
	int height_trans_2 = node->b.normal_tx.height;
	if (height_of_block != height_trans_1 || height_of_block != height_trans_2){
		printf("INI GOBLOK ! TES 3!! \n\n");
		return 0;
	}

	// FOURTH BULLET POINT

	// the prev_transaction_hash in reward_tx must be equal to zero.
	if (byte32_is_zero(node->b.reward_tx.prev_transaction_hash) == 0){
		printf("INI GOBLOK TES 4!!! \n\n");
		return 0;
	}

	// reward_tx.src signature r and signature s must be equal to zero (byte32_is_zero return 1 if true, else zero).
	if (byte32_is_zero(node->b.reward_tx.src_signature.r) == 0 || byte32_is_zero(node->b.reward_tx.src_signature.s) == 0){
		printf("INI GOBLOK  TES 4.2!!! \n\n");
		return 0;
	}

	// FIFTH BULLET POINT
	
	hash_output trans1;
	hash_output trans2;

	if (byte32_is_zero(node->b.normal_tx.prev_transaction_hash) == 0) {

		struct blockchain_node *temp_node = node->parent;
		int tester = 0;

		while (temp_node->parent != temp_node) {

			transaction_hash(&temp_node->b.normal_tx, trans1);
			transaction_hash(&temp_node->b.reward_tx, trans2);

			if(byte32_cmp(node->b.normal_tx.prev_transaction_hash, trans1) == 0 || byte32_cmp(node->b.normal_tx.prev_transaction_hash, trans2) == 0)
				tester = 1;

			temp_node = temp_node->parent;
		}

		if (tester == 0) {
			printf("INI GOBLOK TES 5!!! \n\n");
			return 0;
		}

		// transaction_hash(&node->parent->b.normal_tx, trans1);
		// transaction_hash(&node->parent->b.reward_tx, trans2);

		// if(byte32_cmp(node->b.normal_tx.prev_transaction_hash, trans1) != 0 && byte32_cmp(node->b.normal_tx.prev_transaction_hash, trans2) != 0) {
		// 	printf("INI GOBLOK TES 5!!! \n\n");
		// 	return 0;
		// }
	

	// FIFTH II BULLET POINT
	//The signature on normal_tx must be valid using the dest_pubkey of the previous transaction that has hash value normal_tx.prev_transaction_hash. 
	//(Use the transaction_verify function.)

		hash_output prev_trans1;
		hash_output prev_trans2;

		transaction_hash(&node->parent->b.normal_tx, prev_trans1);
		transaction_hash(&node->parent->b.reward_tx, prev_trans2);

		struct transaction temp_trans1;

		temp_trans1 = node->b.normal_tx;

		if (byte32_cmp(prev_trans1, node->b.normal_tx.prev_transaction_hash) == 0) {
			if (transaction_verify(&(temp_trans1), &node->parent->b.normal_tx) != 1) {
				printf("INI GOBLOK TES 5.2!!! \n\n");
				return 0;
			}
		}

		else if (byte32_cmp(prev_trans2, node->b.normal_tx.prev_transaction_hash) == 0) {
			if (transaction_verify(&(temp_trans1), &node->parent->b.reward_tx) != 1) {
				printf("INI GOBLOK TES 5.3!!! \n\n");
				return 0;
			}
		}

		// LAST BULLET POINT

		struct blockchain_node *dummy_node = node->parent;

		while (dummy_node->parent != dummy_node) {
			if (byte32_cmp(dummy_node->b.normal_tx.prev_transaction_hash, node->b.normal_tx.prev_transaction_hash) == 0) {
				printf("INI GOBLOK  TES 5.4!!! \n\n");
				return 0;
			}
			dummy_node = dummy_node->parent;
		}

	}

    return 1;

}

/* Add or subtract an amount from a linked list of balances. Call it like this:
 *   struct balance *balances = NULL;
 *
 *   // reward_tx increment.
 *   balances = balance_add(balances, &b.reward_tx.dest_pubkey, 1);
 *
 *   // normal_tx increment and decrement.
 *   balances = balance_add(balances, &b.normal_tx.dest_pubkey, 1);
 *   balances = balance_add(balances, &prev_transaction.dest_pubkey, -1);
 */
static struct balance *balance_add(struct balance *balances,
	struct ecdsa_pubkey *pubkey, int amount)
{
	struct balance *p;

	for (p = balances; p != NULL; p = p->next) {
		if ((byte32_cmp(p->pubkey.x, pubkey->x) == 0)
			&& (byte32_cmp(p->pubkey.y, pubkey->y) == 0)) {
			p->balance += amount;
			return balances;
		}
	}

	/* Not found; create a new list element. */
	p = malloc(sizeof(struct balance));
	if (p == NULL)
		return NULL;
	p->pubkey = *pubkey;
	p->balance = amount;
	p->next = balances;

	return p;
}

int main(int argc, char *argv[])
{
	int i;
	int count = 0;
	struct blockchain_node a;

	// Initialize a new array to store the input blocks b
	struct blockchain_node array_of_block[1000];

	/* Read input block files. */
	for (i = 1; i < argc; i++) {
		char *filename;
		struct block b;
		int rc;

		filename = argv[i];
		rc = block_read_filename(&b, filename);
		if (rc != 1) {
			fprintf(stderr, "could not read %s\n", filename);
			exit(1);
		}

		/* TODO */
		/* Feel free to add/modify/delete any code you need to. */

		// save the looping block to array_of_block at index i
		struct blockchain_node x;
		x.b = b;
		x.order = i;

		count ++;
		array_of_block[i] = x;

		// print the height and nonce of block b
		// printf("block b's height: [%u] \n",array_of_block[i].b.height);
		// printf("block b's nonce: [%u] \n",array_of_block[i].b.nonce);

	}

	// sorting an array

	for ( i = 1; i < argc; ++i)
    {
        for (int j = i + 1; j < argc; ++j)
        {
            if (array_of_block[i].b.height > array_of_block[j].b.height)
            {
                a =  array_of_block[i];
                array_of_block[i] = array_of_block[j];
                array_of_block[j] = a;
            }
        }
    }

    // making the tree connections
    for (i=1; i < argc; ++i) {

    	//if genesis block, then the parent is null
    	if (array_of_block[i].b.height == 0){
    		array_of_block[i].parent = &array_of_block[i];
    	}

    	else {
    		int single = 0;
    		for (int p=1; p < argc; ++p) {
    			hash_output parent_hash;
    			block_hash(&array_of_block[p].b, parent_hash);

    			// if block b.prev_block_hash is hash(parent) then assign blockchain_node[i]'s parent to blockhain_node[p].
    			if (byte32_cmp(array_of_block[i].b.prev_block_hash, parent_hash) == 0) {
    				single = 1;
    				array_of_block[i].parent = &array_of_block[p];
    			}
    			if (single == 0)
    				array_of_block[i].parent = &array_of_block[i];

    		}

    	}
    }

    hash_output parent_hash;
    block_hash(&array_of_block[7].b, parent_hash);

    for (i = 1; i < argc; ++i) {
    	printf("block b's height: [%u], block b's parents height: [%u] \n",array_of_block[i].b.height, array_of_block[i].parent->b.height);
    }

    // printf("BLOCK %i \n\n\n", array_of_block[1].parent->b.height);
    
    // Check validness of one block
  //   int num = 0;

  //   array_of_block[1].is_valid = 1;
  //   array_of_block[2].is_valid = 1;
  //   array_of_block[3].is_valid = 1;
  //   array_of_block[4].is_valid = 1;
  //   array_of_block[5].is_valid = 1;
 	// array_of_block[6].is_valid = 0;
 	// array_of_block[7].is_valid = 1;
 	// array_of_block[8].is_valid = 0;
 	// array_of_block[9].is_valid = 1;

  //   int test = validness_test(&array_of_block[num], argc);

  //   if (test == 1)
  //   	printf("TEST[%i] SUCCEED: %i \n",num, test);

  //  	else
  //  		printf("FAIL NGENTOT %i \n\n", test);


   	// ASSIGN VALIDITY TO ALL BLOCKS

   	for (i = 1; i < argc; ++i) {
   		array_of_block[i].is_valid = validness_test(&array_of_block[i], argc);
   	}

   	for (i = 1; i < argc; ++i) {
   		if (array_of_block[i].is_valid == 1)
   			printf("BLOCK[%i] IS VALID!\n",i);
   		else
   			printf("BLOCK[%i] IS NOTTTTT VALID!\n",i);

   	}

	/* Organize into a tree, check validity, and output balances. */
	/* TODO */

	struct balance *balances = NULL, *p, *next;
	/* Print out the list of balances. */
	for (p = balances; p != NULL; p = next) {
		next = p->next;
		printf("%s %d\n", byte32_to_hex(p->pubkey.x), p->balance);
		free(p);
	}

	return 0;
}