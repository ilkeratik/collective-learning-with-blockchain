from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback

from backend.blockchain.block import Block
subscribe_key  = 'sub-c-81caca46-c576-11ec-9f25-82b465a2b170'
publish_key = 'pub-c-3f7756ba-f177-4a54-95ce-8b000c14242a'


pn_conf = PNConfiguration()
pn_conf.subscribe_key = subscribe_key
pn_conf.publish_key = publish_key
pn_conf.uuid = "custom uuid"


CHANNELS = {
    'TEST': 'TEST',
    'BLOCK': 'BLOCK'
}

class Listener(SubscribeCallback):
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def message(self, pubnub, message_object):
        print(f'\-- Channel: {message_object.channel}, Message: {message_object.message}')

        if message_object.channel == CHANNELS['BLOCK']:
            block = Block.from_dict(message_object.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)

            try:
                self.blockchain.replace_chain(potential_chain)
                print(f'\n -- Successfully replaced the local chain')
            except Exception as e:
                print(f'\n -- Did not replace the chain: {e}')


class PubSub():
    """
    Handles the pub/sub layer of the application.
    Provides communication between the nodes of the blockchain network.
    """
    def __init__(self, blockchain):
        self.pubnub = PubNub(pn_conf)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain))

    def publish(self, channel, message):
        """
        Publishes a message to given channel
        """
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block):
        """
        Broadcast a block object to all nodes.
        """
        self.publish(CHANNELS['BLOCK'], block.to_dict())

def main():
    pbs = PubSub()
    pbs.publish(CHANNELS['TEST'], {'FOO': 'BAR'})


if __name__ == '__main__':
    main()